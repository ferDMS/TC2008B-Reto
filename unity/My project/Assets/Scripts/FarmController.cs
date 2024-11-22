using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;
using System.Collections.Generic;
using UnityEngine.Events;

// Define the InitializeData class outside of the coroutine
[System.Serializable]
public class InitializeData
{
    public int plant_grid_size;
    public int path_width;
    public int num_tractors;
    public int water_capacity;
    public int fuel_capacity;
    public int wheat_capacity;
    public int steps;
}

[System.Serializable]
public class StepInfoListWrapper
{
    public List<StepInfo> simulationSteps;
}


public class FarmController : MonoBehaviour
{

    public int plantGridSize = 5;
    public int pathWidth = 2;
    public int numTractors = 2;
    public int waterCapacity = 100;
    public int fuelCapacity = 50;
    public int wheatCapacity = 5;
    public int steps = 10;
    private string apiUrl = "http://localhost:5000/initialize";

    public GameObject planePrefab;
    private GameObject plane;
    public float cellSize = 1.0f;
    public List<StepInfo> stepsList;

    public bool showGridGizmos = true;
    public Color pathColor = Color.red;
    public Color plantAreaColor = Color.green;
    public float gizmoHeight = 0.1f;

    public UnityEvent OnSimulationInitialized = new UnityEvent();

    public StepInfo GetStepInfo(int step)
    {
        if(step >= 0 && step < stepsList.Count)
        {
            return stepsList[step];
        }
        return null;
    }

    void Start()
    {
        Debug.Log($"Starting FarmController with values: Grid Size={plantGridSize}, Path Width={pathWidth}, Num Tractors={numTractors}");
        InitializePlane();
        StartCoroutine(SendDataToAPI());
    }

    void InitializePlane()
    {
        if (planePrefab == null)
        {
            Debug.LogError("Plane prefab not assigned! Please assign it in the Unity Inspector.");
            return;
        }

        int totalGridSize = plantGridSize + (pathWidth * 2);

        plane = Instantiate(planePrefab, Vector3.zero, Quaternion.identity);
        plane.transform.parent = this.transform; 

        float desiredWidth = totalGridSize * cellSize;
        float scaleFactor = desiredWidth / 10f;
        
        plane.transform.localScale = new Vector3(scaleFactor, 1f, scaleFactor);
        plane.transform.position = new Vector3(0f, 0f, 0f);

        Debug.Log($"Initialized plane with scale: {scaleFactor} for grid size: {totalGridSize}");
    }

    
    IEnumerator SendDataToAPI()
    {
        InitializeData data = new InitializeData
        {
            plant_grid_size = plantGridSize,
            path_width = pathWidth,
            num_tractors = numTractors,
            water_capacity = waterCapacity,
            fuel_capacity = fuelCapacity,
            wheat_capacity = wheatCapacity,
            steps = steps
        };

        string jsonData = JsonUtility.ToJson(data);
        Debug.Log("Sending Data: " + jsonData);

        var request = new UnityWebRequest(apiUrl, "POST")
        {
            uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(jsonData)),
            downloadHandler = new DownloadHandlerBuffer()
        };
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
            Debug.LogError($"Response: {request.downloadHandler.text}");
            yield break;  // Correctly terminating the coroutine on error
        }

        Debug.Log("Received: " + request.downloadHandler.text);
        try
        {
            string json = $"{{\"simulationSteps\":{request.downloadHandler.text}}}";
            var wrapper = JsonUtility.FromJson<StepInfoListWrapper>(json);

            stepsList = wrapper.simulationSteps;

            foreach (var step in stepsList)
            {
                foreach (var tractor in step.tractors)
                {
                   Debug.Log($"Step {step.step}: Tractor at position {tractor.tractorPosition}");
                }
              
            }
            Debug.Log($"Processed {stepsList.Count} steps");
            OnSimulationInitialized.Invoke();
        }
        catch (System.Exception e)
        {
            Debug.LogError("Error parsing JSON: " + e.Message);
            yield break;  // Correctly terminating the coroutine on exception
        }
    }

    public Vector3 GetWorldPositionFromGrid(int x, int z)
    {
        int totalGridSize = plantGridSize + (pathWidth * 2);
        float gridWorldSize = totalGridSize * cellSize;
        float halfGridSize = gridWorldSize / 2f;

        float xPos = (x * cellSize) - halfGridSize + (cellSize / 2f);
        float zPos = (z * cellSize) - halfGridSize + (cellSize / 2f);

        return new Vector3(xPos, 0f, zPos);
    }

    public int GetTotalSteps()
    {
        return stepsList.Count;
    }


    void OnDrawGizmos()
    {
        if (!showGridGizmos) return;

        int totalGridSize = plantGridSize + (pathWidth * 2);
        Vector3 centerOffset = new Vector3(totalGridSize * cellSize / 2f, 0, totalGridSize * cellSize / 2f);

        for (int x = 0; x < totalGridSize; x++)
        {
            for (int z = 0; z < totalGridSize; z++)
            {
                // Determine if this is a path or plant area
                bool isPath = x < pathWidth || x >= totalGridSize - pathWidth || 
                            z < pathWidth || z >= totalGridSize - pathWidth;

                // Set color based on area type
                Gizmos.color = isPath ? pathColor : plantAreaColor;

                // Calculate position
                Vector3 position = GetWorldPositionFromGrid(x, z);
                
                // Draw cube
                Gizmos.DrawWireCube(position + Vector3.up * (gizmoHeight / 2f), 
                    new Vector3(cellSize, gizmoHeight, cellSize));

                // Optionally draw position labels for debugging
                #if UNITY_EDITOR
                UnityEditor.Handles.Label(position + Vector3.up * gizmoHeight, 
                    $"({x},{z})");
                #endif
            }
        }
    }
}

