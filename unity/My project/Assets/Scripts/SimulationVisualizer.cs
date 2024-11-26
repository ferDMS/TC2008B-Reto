using UnityEngine;
using System.Collections.Generic;
using System.Collections;

public class SimulationVisualizer : MonoBehaviour
{
    [Header("Prefabs")]
    public GameObject tractorPrefab;
    public GameObject plantPrefab;

    [Header("Visualization Settings")]
    public float moveSpeed = 5f;
    public float stepDelay = 1f;

    [Header("Height Offsets")]
    public float tractorHeight = 1f;
    public float plantHeight = 0f;

    private FarmController farmController;
    private Dictionary<int, GameObject> tractors = new Dictionary<int, GameObject>();
    private Dictionary<Vector2Int, GameObject> plants = new Dictionary<Vector2Int, GameObject>();
    private List<TractorController> tractorControllers = new List<TractorController>();
    private HashSet<Vector2Int> harvestedPositions = new HashSet<Vector2Int>();

    private bool isSimulationRunning = false;
    private int currentStep = 0;
    private float currentStepDelay;  // Added this line

    void Start()
    {
        farmController = GetComponent<FarmController>();
        if (farmController == null)
        {
            Debug.LogError("FarmController not found!");
            return;
        }
        currentStepDelay = stepDelay;  // Initialize in Start
        farmController.OnSimulationInitialized.AddListener(InitializeVisualization);
    }

    void InitializeVisualization()
    {
        Debug.Log("Initializing Visualization");
        ClearExistingObjects();
        harvestedPositions.Clear();
        CreatePlants();
        CreateTractors();
        StartCoroutine(RunSimulation());
    }

    void ClearExistingObjects()
    {
        foreach (var tractor in tractors.Values)
        {
            if (tractor != null) Destroy(tractor);
        }
        foreach (var plant in plants.Values)
        {
            if (plant != null) Destroy(plant);
        }
        tractors.Clear();
        plants.Clear();
        tractorControllers.Clear();
        harvestedPositions.Clear();
    }

    void CreatePlants()
    {
        if (plantPrefab == null)
        {
            Debug.LogError("Plant prefab not assigned!");
            return;
        }

        GameObject plantsParent = new GameObject("Plants");
        plantsParent.transform.parent = transform;

        int pathWidth = farmController.pathWidth;
        int plantGridSize = farmController.plantGridSize;
        int totalGridSize = plantGridSize + (pathWidth * 2);

        Debug.Log($"Creating plants with pathWidth: {pathWidth}, plantGridSize: {plantGridSize}, totalGridSize: {totalGridSize}");

        for (int x = pathWidth; x < totalGridSize - pathWidth; x++)
        {
            for (int z = pathWidth; z < totalGridSize - pathWidth; z++)
            {
                Vector2Int gridPos = new Vector2Int(x, z);
                Vector3 worldPos = farmController.GetWorldPositionFromGrid(x, z);
                worldPos.y += plantHeight;

                GameObject plant = Instantiate(plantPrefab, worldPos, Quaternion.identity);
                plant.transform.parent = plantsParent.transform;
                plant.name = $"Plant_{x}_{z}";
                plants[gridPos] = plant;
                Debug.Log($"Created plant at position ({x}, {z})");
            }
        }
        Debug.Log($"Created total of {plants.Count} plants");
    }

    void CreateTractors()
    {
        if (tractorPrefab == null)
        {
            Debug.LogError("Tractor prefab not assigned!");
            return;
        }

        GameObject tractorsParent = new GameObject("Tractors");
        tractorsParent.transform.parent = transform;
        
        StepInfo firstStep = farmController.GetStepInfo(0);
        if (firstStep == null)
        {
            Debug.LogError("No initial step info available!");
            return;
        }

        Debug.Log($"Creating {farmController.numTractors} tractors");
        for (int i = 0; i < farmController.numTractors; i++)
        {
            Vector2Int tractorPos = firstStep.GetTractorPosition(i);
            Vector3 startPos = farmController.GetWorldPositionFromGrid(tractorPos.x, tractorPos.y);
            startPos.y += tractorHeight;

            GameObject tractor = Instantiate(tractorPrefab, startPos, Quaternion.identity);
            tractor.transform.parent = tractorsParent.transform;
            tractor.name = $"Tractor_{i}";
            tractors[i] = tractor;

            TractorController tractorController = tractor.GetComponent<TractorController>();
            if (tractorController == null)
            {
                tractorController = tractor.AddComponent<TractorController>();
            }

            tractorController.moveSpeed = moveSpeed;
            tractorController.targetPosition = startPos;
            tractorController.tractorId = i;
            tractorController.OnTractorReachedTarget += HandleTractorReachedTarget;
            tractorController.gridPosition = firstStep.GetTractorPosition(i);
            tractorController.currentTask = firstStep.GetTractorTask(i);

            // Initialize resource levels
            TractorInfo tractorInfo = firstStep.tractors[i];
            tractorController.UpdateResources(
                tractorInfo.water_level,
                tractorInfo.fuel_level,
                tractorInfo.wheat_level
            );

            tractorControllers.Add(tractorController);
            Debug.Log($"Created Tractor {i} at position {tractorPos}");
        }
    }

    IEnumerator RunSimulation()
    {
        if (isSimulationRunning)
        {
            Debug.LogWarning("Simulation already running!");
            yield break;
        }

        Debug.Log("Starting simulation");
        isSimulationRunning = true;
        currentStep = 0;
        harvestedPositions.Clear(); // Clear harvested positions at start
        int totalSteps = farmController.GetTotalSteps();

        while (currentStep < totalSteps)
        {
            StepInfo stepInfo = farmController.GetStepInfo(currentStep);
            if (stepInfo == null)
            {
                Debug.LogError($"No step info for step {currentStep}");
                break;
            }

            Debug.Log($"Processing step {currentStep}/{totalSteps}");
            
            foreach (var controller in tractorControllers)
            {
                int tractorId = controller.tractorId;
                TractorInfo tractorInfo = stepInfo.tractors[tractorId];
                
                Vector2Int newPos = new Vector2Int(tractorInfo.position[0], tractorInfo.position[1]);
                Vector3 targetPos = farmController.GetWorldPositionFromGrid(newPos.x, newPos.y);
                targetPos.y += tractorHeight;

                controller.targetPosition = targetPos;
                controller.gridPosition = newPos;
                controller.currentTask = tractorInfo.task;
                controller.UpdateResources(
                    tractorInfo.water_level,
                    tractorInfo.fuel_level,
                    tractorInfo.wheat_level
                );

                Debug.Log($"Tractor {tractorId} at step {currentStep}: Position: {newPos}, Task: {tractorInfo.task}");
            }

            yield return new WaitForSeconds(currentStepDelay);
            currentStep++;
        }

        Debug.Log($"Simulation complete. Remaining plants: {plants.Count}");
        isSimulationRunning = false;
    }

    private void HandleTractorReachedTarget(Vector2Int gridPosition, int tractorId, string task)
    {
        Debug.Log($"Tractor {tractorId} reached position {gridPosition} with task: {task}");

        if (!plants.ContainsKey(gridPosition))
        {
            Debug.Log($"No plant found at position {gridPosition}");
            return;
        }

        GameObject plant = plants[gridPosition];
        TractorController tractor = tractorControllers[tractorId];

        switch (task.ToLower())
        {
            case "watering":
                if (tractor.waterLevel > 0)
                {
                    var renderers = plant.GetComponentsInChildren<MeshRenderer>();
                    foreach (var renderer in renderers)
                    {
                        Material newMaterial = new Material(renderer.material);
                        newMaterial.color = Color.blue;
                        renderer.material = newMaterial;
                    }
                    Debug.Log($"Tractor {tractorId} watered plant at {gridPosition}");
                }
                break;

            case "harvesting":
                if (tractor.wheatLevel < farmController.wheatCapacity && !harvestedPositions.Contains(gridPosition))
                {
                    Debug.Log($"Harvesting plant at {gridPosition}");
                    Destroy(plant);
                    plants.Remove(gridPosition);
                    harvestedPositions.Add(gridPosition);
                    Debug.Log($"Tractor {tractorId} harvested plant at {gridPosition}. Remaining plants: {plants.Count}");
                }
                break;

            case "depositing":
                Debug.Log($"Tractor {tractorId} depositing at {gridPosition}");
                break;
        }
    }

    public void RestartSimulation()
    {
        StopAllCoroutines();
        isSimulationRunning = false;
        InitializeVisualization();
    }

    void OnDisable()
    {
        StopAllCoroutines();
        isSimulationRunning = false;
    }
}