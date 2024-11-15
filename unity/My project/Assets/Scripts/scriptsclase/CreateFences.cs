using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateFences : MonoBehaviour
{
    public GameObject fencePrefab; // Prefab for the fence object
    public float fenceLength = 3.0f; // Length of each fence segment
    public float areaSize = 30.0f; // Size of the grass area

    // Start is called before the first frame update
    void Start()
    {
        SurroundGrassWithFence();
    }

    void SurroundGrassWithFence()
    {
        if (fencePrefab == null)
        {
            Debug.LogError("Fence Prefab is not assigned.");
            return;
        }

        // Calculate positions for the fence segments
        Vector3[] fencePositions = CalculateFencePositions(areaSize, fenceLength);

        // Instantiate fence segments at calculated positions
        foreach (Vector3 position in fencePositions)
        {
            Quaternion rotation = CalculateFenceRotation(position);
            Instantiate(fencePrefab, position, rotation);
        }
    }

    Vector3[] CalculateFencePositions(float areaSize, float fenceLength)
    {
        List<Vector3> positions = new List<Vector3>();

        // Calculate positions along the perimeter of the grass area
        for (float x = -areaSize; x <= areaSize; x += fenceLength)
        {
            positions.Add(new Vector3(x, 0, -areaSize));
            positions.Add(new Vector3(x, 0, areaSize));
        }

        for (float z = -areaSize; z <= areaSize; z += fenceLength)
        {
            positions.Add(new Vector3(-areaSize, 0, z));
            positions.Add(new Vector3(areaSize, 0, z));
        }

        return positions.ToArray();
    }

    Quaternion CalculateFenceRotation(Vector3 position)
    {
        if (Mathf.Approximately(position.z, -areaSize) || Mathf.Approximately(position.z, areaSize))
        {
            return Quaternion.Euler(0, 90, 0); // Rotate 90 degrees for fences along the z-axis
        }
        return Quaternion.identity; // No rotation for fences along the x-axis
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
