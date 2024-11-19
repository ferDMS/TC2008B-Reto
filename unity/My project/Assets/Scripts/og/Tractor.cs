// Tractor.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tractor : MonoBehaviour
{

    public TractorTask CurrentTask { get; set; }
    public Vector2Int Position { get; set; }

    [SerializeField] private int waterCapacity = 20;
    [SerializeField] private int fuelCapacity = 100;
    [SerializeField] private int wheatCapacity = 5;

   
    public int WaterLevel { get; private set; }
    public int FuelLevel { get; private set; }
    public int WheatLevel { get; private set; }

    public float moveSpeed = 2f;

    // References
    private FarmMap farmMap;
    private Pathfinding pathfinder;
    private List<Vector2Int> currentPath;
    private int pathIndex = 0;
    private Vector3 targetWorldPos;

    // Properties
    public int WaterCapacity => waterCapacity;
    public int FuelCapacity => fuelCapacity;
    public int WheatCapacity => wheatCapacity;

    protected virtual void Start()
    {
        // Initialize levels
        WaterLevel = waterCapacity;
        FuelLevel = fuelCapacity;
        WheatLevel = 0;
        CurrentTask = TractorTask.Idle;

        // Get references
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

    public void AssignTask(TractorTask task, Vector3 targetWorldPos)
    {
        CurrentTask = task;
        this.targetWorldPos = targetWorldPos;
        Vector2Int targetFarmPos = farmMap.WorldToFarmPosition(targetWorldPos);
        StartCoroutine(FindAndFollowPath(targetFarmPos));
    }

    private IEnumerator FindAndFollowPath(Vector2Int targetFarmPos)
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

    private void PerformTask()
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
                break;
        }
        CurrentTask = TractorTask.Idle;
    }

    private void WaterPlant()
    {
        Plant plant = FarmModel.Instance.GetPlantAtPosition(Position);
        if (plant != null && plant.NeedsWater() && WaterLevel > 0)
        {
            plant.Water();
            UseWater();
            Debug.Log($"{gameObject.name} watered plant at {Position}.");
        }
    }

    private void HarvestPlant()
    {
        Plant plant = FarmModel.Instance.GetPlantAtPosition(Position);
        if (plant != null && plant.IsReadyForHarvest() && WheatLevel < WheatCapacity)
        {
            plant.Harvest();
            CollectWheat();
            Debug.Log($"{gameObject.name} harvested plant at {Position}.");
        }
    }

    public void DepositWheat()
    {
        Silo silo = FarmModel.Instance.Silo;
        if (silo != null && WheatLevel > 0)
        {
            silo.DepositWheat(WheatLevel);
            WheatLevel = 0;
            Debug.Log($"{gameObject.name} deposited wheat to the silo.");
        }
    }

    public void UseWater()
    {
        WaterLevel = Mathf.Max(0, WaterLevel - 1);
    }

    public void CollectWheat()
    {
        if (WheatLevel < WheatCapacity)
        {
            WheatLevel++;
        }
    }

    public void ConsumeFuel()
    {
        FuelLevel = Mathf.Max(0, FuelLevel - 1);
    }
}
