// FarmModel.cs
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class FarmModel : MonoBehaviour
{
    public static FarmModel Instance;

    [Header("Farm Settings")]
    public int FarmWidth = 20; 
    public int FarmHeight = 20;

    [Header("Agent Collections")]
    public List<Plant> Plants;
    public List<Tractor> Tractors;
    public Silo Silo;

    [Header("Prefabs")]
    public GameObject PlantPrefab;
    public GameObject TractorPrefab;
    public GameObject SiloPrefab;

    // Occupied cells tracking
    private HashSet<Vector2Int> OccupiedCells = new HashSet<Vector2Int>();

    [Header("Simulation Settings")]
    public int Steps = 200;
    private int currentStep = 0;
    public float StepsPerSecond = 2f;
    private float stepTimer = 0f;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    void Start()
    {
        InitializeFarm();
    }

    void InitializeFarm()
    {
        InitializePlants();
        InitializeSilo();
        InitializeTractors();
    }

    void InitializePlants()
    {
        Plants = new List<Plant>();
        FarmMap farmMap = FindObjectOfType<FarmMap>();
        for (int y = 0; y < FarmHeight; y++)
        {
            for (int x = 0; x < FarmWidth; x++)
            {
                Vector2Int pos = new Vector2Int(x, y);
                Vector3 worldPos = farmMap.FarmToWorldPosition(x, y);
                GameObject plantObj = Instantiate(PlantPrefab, worldPos, Quaternion.identity);
                Plant plant = plantObj.GetComponent<Plant>();
                plant.Position = pos;
                Plants.Add(plant);
            }
        }
    }

    void InitializeSilo()
    {
        FarmMap farmMap = FindObjectOfType<FarmMap>();
        Vector2Int siloPos = new Vector2Int(FarmWidth - 1, 0); // Top-right corner
        Vector3 siloWorldPos = farmMap.FarmToWorldPosition(siloPos.x, siloPos.y);
        GameObject siloObj = Instantiate(SiloPrefab, siloWorldPos, Quaternion.identity);
        Silo = siloObj.GetComponent<Silo>();
        Silo.Position = siloPos;
    }

    void InitializeTractors()
    {
        Tractors = new List<Tractor>();
        FarmMap farmMap = FindObjectOfType<FarmMap>();
        Pathfinding pathfinder = FindObjectOfType<Pathfinding>();

        int numTractors = 4; // Example: 4 tractors
        for (int i = 0; i < numTractors; i++)
        {
            // Select random walkable position
            Vector2Int pos = new Vector2Int(Random.Range(0, FarmWidth), Random.Range(0, FarmHeight));
            while (Tractors.Any(t => t.Position == pos) || !farmMap.IsWalkable(pos.x, pos.y))
            {
                pos = new Vector2Int(Random.Range(0, FarmWidth), Random.Range(0, FarmHeight));
            }

            Vector3 tractorWorldPos = farmMap.FarmToWorldPosition(pos.x, pos.y);
            GameObject tractorObj = Instantiate(TractorPrefab, tractorWorldPos, Quaternion.identity);
            Tractor tractor = tractorObj.GetComponent<Tractor>();
            tractor.Position = pos;
            Tractors.Add(tractor);

            // Occupy the initial position
            OccupyCell(pos);
        }
    }

    // Retrieve a plant at a specific farm position
    public Plant GetPlantAtPosition(Vector2Int position)
    {
        return Plants.FirstOrDefault(p => p.Position == position && !p.Harvested);
    }

    // Occupy a cell to prevent other tractors from moving into it
    public void OccupyCell(Vector2Int cell)
    {
        OccupiedCells.Add(cell);
    }

    // Vacate a cell when a tractor leaves it
    public void VacateCell(Vector2Int cell)
    {
        OccupiedCells.Remove(cell);
    }

    // Check if a cell is traversable (not occupied)
    public bool IsCellTraversable(Vector2Int cell)
    {
        return !OccupiedCells.Contains(cell);
    }

    // Retrieve neighboring cells for pathfinding
    public List<Vector2Int> GetNeighbors(Vector2Int cell)
    {
        List<Vector2Int> neighbors = new List<Vector2Int>
        {
            new Vector2Int(cell.x + 1, cell.y),
            new Vector2Int(cell.x - 1, cell.y),
            new Vector2Int(cell.x, cell.y + 1),
            new Vector2Int(cell.x, cell.y - 1)
            // Add diagonals if needed
        };

        return neighbors.Where(n => IsWithinFarm(n)).ToList();
    }

    // Check if a cell is within farm boundaries
    public bool IsWithinFarm(Vector2Int cell)
    {
        return cell.x >= 0 && cell.x < FarmWidth && cell.y >= 0 && cell.y < FarmHeight;
    }

    void Update()
    {
        if (currentStep >= Steps)
            return;

        stepTimer += Time.deltaTime;
        if (stepTimer >= 1f / StepsPerSecond)
        {
            StepSimulation();
            currentStep++;
            stepTimer = 0f;
        }
    }

    void StepSimulation()
    {
        GrowPlants();
        AssignTractorTasks();
        UpdateUI();
    }

    void GrowPlants()
    {
        foreach (var plant in Plants)
        {
            plant.Grow();
        }
    }

    void AssignTractorTasks()
    {
        foreach (var tractor in Tractors)
        {
            if (tractor.CurrentTask != TractorTask.Idle)
                continue; // Skip if already assigned

            if (tractor.FuelLevel <= 0)
            {
                tractor.CurrentTask = TractorTask.Idle;
                continue;
            }

            if (tractor.WheatLevel >= tractor.WheatCapacity)
            {
                tractor.AssignTask(TractorTask.Depositing, Silo.transform.position);
            }
            else
            {
                Plant targetPlant = Plants.FirstOrDefault(p => p.NeedsWater());
                if (targetPlant != null)
                {
                    tractor.AssignTask(TractorTask.Watering, targetPlant.transform.position);
                }
                else
                {
                    targetPlant = Plants.FirstOrDefault(p => p.IsReadyForHarvest());
                    if (targetPlant != null)
                    {
                        tractor.AssignTask(TractorTask.Harvesting, targetPlant.transform.position);
                    }
                    else
                    {
                        tractor.CurrentTask = TractorTask.Idle;
                    }
                }
            }
        }
    }

    void UpdateUI()
    {
        // Implement UI updates here, e.g., using UIManager
        if (UIManager.Instance != null)
        {
            UIManager.Instance.UpdateStep(currentStep, Steps);
            UIManager.Instance.UpdateTractorInfo(Tractors);
            UIManager.Instance.UpdatePlantInfo(Plants);
        }
    }
}
