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
    public float tractorHeight = 1f; // Height offset for tractor from ground
    public float plantHeight = 0f;     // Height offset for plants from ground

    private FarmController farmController;
    private Dictionary<int, GameObject> tractors = new Dictionary<int, GameObject>();
    private Dictionary<Vector2Int, GameObject> plants = new Dictionary<Vector2Int, GameObject>();
    private bool isSimulationRunning = false;

    private int currentStep = 0;
    

    void Start()
    {
        // Get reference to the FarmController
        farmController = GetComponent<FarmController>();
        if (farmController == null)
        {
            Debug.LogError("FarmController not found!");
            return;
        }

        // Subscribe to the initialization event
        farmController.OnSimulationInitialized.AddListener(InitializeVisualization);
    }

    void InitializeVisualization()
    {
        CreatePlants();
        CreateTractors();
        StartCoroutine(RunSimulation());
    }

    void CreatePlants()
    {
        if (plantPrefab == null)
        {
            Debug.LogError("Plant prefab not assigned!");
            return;
        }

        // Create a parent object for plants
        GameObject plantsParent = new GameObject("Plants");
        plantsParent.transform.parent = transform;

        // Calculate the plant area boundaries
        int pathWidth = farmController.pathWidth;
        int plantGridSize = farmController.plantGridSize;
        int totalGridSize = plantGridSize + (pathWidth * 2);

        // Create plants in the inner grid (excluding paths)
        for (int x = pathWidth; x < totalGridSize - pathWidth; x++)
        {
            for (int z = pathWidth; z < totalGridSize - pathWidth; z++)
            {
                Vector2Int gridPos = new Vector2Int(x, z);
                Vector3 worldPos = farmController.GetWorldPositionFromGrid(x, z);
                worldPos.y += plantHeight; // Add height offset

                GameObject plant = Instantiate(plantPrefab, worldPos, Quaternion.identity);
                plant.transform.parent = plantsParent.transform;
                plant.name = $"Plant_{x}_{z}";
                plants[gridPos] = plant;

                // Add visual debug component
                //plant.AddComponent<PositionDebugger>().SetGridPosition(gridPos);
            }
        }
    }

    void CreateTractors()
    {
        if (tractorPrefab == null)
        {
            Debug.LogError("Tractor prefab not assigned!");
            return;
        }

        // Create a parent object for tractors
        GameObject tractorsParent = new GameObject("Tractors");
        tractorsParent.transform.parent = transform;
        
        StepInfo firstStep = farmController.GetStepInfo(0);
        for(int i = 0; i < farmController.numTractors; i++) {
            // Get the specific position for this tractor from the step info
            Vector2Int tractorPos = firstStep.GetTractorPosition(i);
            
            Vector3 startPos = farmController.GetWorldPositionFromGrid(
                tractorPos.x, 
                tractorPos.y
            );
            startPos.y += tractorHeight;

            GameObject tractor = Instantiate(tractorPrefab, startPos, Quaternion.identity);
            tractor.transform.parent = tractorsParent.transform;
            tractor.name = "Tractor_" + i;
            tractors[i] = tractor;

            // Add tractor controller
            TractorController tractorController = tractor.AddComponent<TractorController>();
            tractorController.moveSpeed = moveSpeed;
            tractorController.targetPosition = startPos;

            tractorController.tractorId = i;
            tractorController.OnTractorReachedTarget += HandleTractorReachedTarget;

            tractorController.gridPosition = firstStep.GetTractorPosition(i);
            tractorController.currentTask = firstStep.GetTractorTask(i);
        }
    }
    

    IEnumerator RunSimulation()
    {
        if (isSimulationRunning) yield break;
        isSimulationRunning = true;

        currentStep = 0;
        int totalSteps = farmController.GetTotalSteps();

        while (currentStep < totalSteps)
        {
            StepInfo stepInfo = farmController.GetStepInfo(currentStep);

            if (stepInfo != null)
            {
                // Handle all tractors
                for (int i = 0; i < farmController.numTractors; i++)
                {
                    if (tractors.ContainsKey(i))
                    {
                        GameObject tractor = tractors[i];
                        TractorController tractorController = tractor.GetComponent<TractorController>();

                        Vector2Int tractorPos = stepInfo.GetTractorPosition(i);
                        Vector3 targetPos = farmController.GetWorldPositionFromGrid(
                            tractorPos.x,
                            tractorPos.y
                        );
                        targetPos.y += tractorHeight;

                        tractorController.targetPosition = targetPos;
                        
                        // // Smoothly move the tractor
                        // while (Vector3.Distance(tractor.transform.position, targetPos) > 0.01f)
                        // {
                        //     tractor.transform.position = Vector3.MoveTowards(
                        //         tractor.transform.position,
                        //         targetPos,
                        //         moveSpeed * Time.deltaTime
                        //     );

                        //     // Rotate tractor to face movement direction
                        //     Vector3 moveDirection = (targetPos - tractor.transform.position).normalized;
                        //     if (moveDirection != Vector3.zero)
                        //     {
                        //         Quaternion targetRotation = Quaternion.LookRotation(moveDirection);
                        //         tractor.transform.rotation = Quaternion.Slerp(
                        //             tractor.transform.rotation,
                        //             targetRotation,
                        //             moveSpeed * Time.deltaTime
                        //         );
                        //     }

                        //     yield return null;
                        // }

                        tractorController.targetPosition = targetPos;
                        tractorController.gridPosition = tractorPos;

                        tractorController.currentTask = stepInfo.GetTractorTask(i);

                        // Update tractor visual state based on task
                        UpdateTractorVisuals(tractor, stepInfo, i);
                    }
                }
            }

            yield return new WaitForSeconds(stepDelay);
            currentStep++;
        }

        isSimulationRunning = false;
    }

    private void HandleTractorReachedTarget(Vector2Int gridPosition, int tractorId, string task) {
        Debug.Log($"Tractor {tractorId} has reached its target");

        if(plants.ContainsKey(gridPosition)) {

            GameObject plant = plants[gridPosition];

            switch (task)
            {
                
                case "watering":
                    // Change the color of the plant to indicate watering
                    //MeshRenderer renderer = plant.GetComponentInChildren<MeshRenderer>();
                    MeshRenderer[] renderers = plant.GetComponentsInChildren<MeshRenderer>();
                    if(renderers.Length > 0) {
                        foreach (MeshRenderer renderer in renderers) {
                            Material newMaterial = new Material(renderer.material);
                            newMaterial.color = Color.blue;
                            renderer.material = newMaterial;
                        }
                    }
                    Debug.Log($"Tractor {tractorId} watered plant at {gridPosition}");
                    break;
                case "harvesting":
                    // Destroy the plant
                    Destroy(plant);
                    plants.Remove(gridPosition);
                    Debug.Log($"Tractor {tractorId} harvested plant at {gridPosition}");
                    break;
            }
        }
    }

    void UpdateTractorVisuals(GameObject tractor, StepInfo stepInfo, int tractorId)
    {
        // You can add visual feedback based on the tractor's task
        // For example, different particle effects or color changes
        switch (stepInfo.GetTractorTask(tractorId))
        {
            case "watering":
                // Maybe activate a water particle system
                Debug.Log($"Tractor {tractorId} is watering");
                break;
            case "harvesting":
                // Maybe activate a harvesting animation
                Debug.Log($"Tractor {tractorId} is harvesting");
                break;
            case "depositing":
                // Maybe change the tractor's appearance to show it's carrying wheat
                Debug.Log($"Tractor {tractorId} is depositing");
                break;
        }

        // You could also update UI elements showing water and fuel levels
        // This would require adding UI elements to your scene
    }

    public void RestartSimulation()
    {
        StopAllCoroutines();
        isSimulationRunning = false;
        StartCoroutine(RunSimulation());
    }
}

// public class PositionDebugger : MonoBehaviour
// {
//     private Vector2Int gridPosition;

//     public void SetGridPosition(Vector2Int pos)
//     {
//         gridPosition = pos;
//     }

//     void OnDrawGizmos()
//     {
//         // Draw a vertical line from the object to the ground
//         Gizmos.color = Color.yellow;
//         Vector3 position = transform.position;
//         Gizmos.DrawLine(position, new Vector3(position.x, 0, position.z));

//         // Draw position text
//         #if UNITY_EDITOR
//         UnityEditor.Handles.Label(position + Vector3.up * 0.5f, 
//             $"Grid: {gridPosition.x},{gridPosition.y}\nWorld: {position}");
//         #endif
//     }
// }



