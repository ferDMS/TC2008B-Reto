// Tractor.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tractor : BaseTractor
{
    [Header("Movement Settings")]
    public float moveSpeed = 2f;

    private FarmMap farmMap;
    private Pathfinding pathfinder;
    private List<Vector2Int> currentPath;
    private int pathIndex = 0;
    private Vector3 targetWorldPos;

    void Start()
    {
        base.Start(); // Initialize base class properties
        farmMap = FindObjectOfType<FarmMap>();
        pathfinder = FindObjectOfType<Pathfinding>();
        Position = farmMap.WorldToFarmPosition(transform.position);
    }

    void Update()
    {
        if (currentPath != null && pathIndex < currentPath.Count)
        {
            Vector3 targetPos = farmMap.FarmToWorldPosition(currentPath[pathIndex].x, currentPath[pathIndex].y);

            targetPos.y = transform.position.y; // Maintain current Y position

            // Move towards the target position
            transform.position = Vector3.MoveTowards(transform.position, targetPos, moveSpeed * Time.deltaTime);

            // Check if reached the target position
            if (Vector3.Distance(transform.position, targetPos) < 0.1f)
            {
                pathIndex++;
                if (pathIndex < currentPath.Count)
                {
                    Position = currentPath[pathIndex - 1];
                }
            }
        }
        else
        {
            // Path completed, perform task
            PerformTask();
        }
    }

    public override void AssignTask(TractorTask task, Vector3 targetWorldPos)
    {
        CurrentTask = task;
        this.targetWorldPos = targetWorldPos;
        Vector2Int targetFarmPos = farmMap.WorldToFarmPosition(targetWorldPos);
        StartCoroutine(FindAndFollowPath(targetFarmPos));
    }

    IEnumerator FindAndFollowPath(Vector2Int targetFarmPos)
    {
        List<Vector2Int> path = pathfinder.FindPath(Position, targetFarmPos);
        if (path.Count == 0)
        {
            Debug.Log($"{gameObject.name}: No path found to target.");
            CurrentTask = TractorTask.Idle;
            yield break;
        }
        currentPath = path;
        pathIndex = 0;

        // Reserve the target cell to avoid collisions
        FarmModel.Instance.OccupyCell(targetFarmPos);

        yield return null;
    }

    public override void PerformTask()
    {
        switch (CurrentTask)
        {
            case TractorTask.Watering:
                WaterPlant();
                break;
            case TractorTask.Harvesting:
                HarvestPlant();
                break;
            case TractorTask.Depositing:
                DepositWheat();
                break;
            case TractorTask.Idle:
            default:
                // Optionally, assign a new task or remain idle
                break;
        }
        CurrentTask = TractorTask.Idle;
    }

    void WaterPlant()
    {
        Plant plant = FarmModel.Instance.GetPlantAtPosition(Position);
        if (plant != null && plant.NeedsWater())
        {
            plant.Watered = true;
            WaterLevel--;
            Debug.Log($"{gameObject.name} watered plant at {Position}.");
        }
    }

    void HarvestPlant()
    {
        Plant plant = FarmModel.Instance.GetPlantAtPosition(Position);
        if (plant != null && plant.IsReadyForHarvest())
        {
            plant.Harvested = true;
            WheatLevel++;
            Debug.Log($"{gameObject.name} harvested plant at {Position}.");
        }
    }

    void DepositWheat()
    {
        Silo silo = FarmModel.Instance.Silo;
        if (silo != null)
        {
            silo.DepositWheat(WheatLevel);
            Debug.Log($"{gameObject.name} deposited wheat to the silo.");
            WheatLevel = 0;
        }
    }
}
