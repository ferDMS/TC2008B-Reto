// FarmMap.cs
using UnityEngine;

public class FarmMap : MonoBehaviour
{
    [Header("Map Dimensions")]
    public int width = 10;
    public int height = 10;
    public float cellSize = 5f;

    [Header("Tractor Settings")]
    public int numTractors = 1;

    public LayerMask obstacleMask;

    private bool[,] walkable;

    void Start()
    {
        InitializeMap();
    }

    void InitializeMap()
    {
        walkable = new bool[width, height];
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Vector3 worldPos = FarmToWorldPosition(x, y);
                walkable[x, y] = !Physics.CheckSphere(worldPos, cellSize / 2f, obstacleMask);
            }
        }
    }

    public Vector3 FarmToWorldPosition(int x, int y)
    {
        return new Vector3(x * cellSize, 0, y * cellSize);
    }

    public bool IsWalkable(int x, int y)
    {
        if (x < 0 || x >= width || y < 0 || y >= height)
            return false;
        return walkable[x, y];
    }

    public Vector2Int WorldToFarmPosition(Vector3 worldPos)
    {
        int x = Mathf.RoundToInt(worldPos.x / cellSize);
        int y = Mathf.RoundToInt(worldPos.z / cellSize);
        return new Vector2Int(x, y);
    }

    void OnDrawGizmos()
    {
        if (walkable == null)
            return;

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Vector3 worldPos = FarmToWorldPosition(x, y);
                Gizmos.color = walkable[x, y] ? Color.green : Color.red;
                Gizmos.DrawLine(worldPos, worldPos + Vector3.right * cellSize);
                Gizmos.DrawLine(worldPos, worldPos + Vector3.forward * cellSize);
            }
        }

        // Draw the outer border lines
        Gizmos.color = Color.white;
        for (int x = 0; x <= width; x++)
        {
            Vector3 start = FarmToWorldPosition(x, 0);
            Vector3 end = FarmToWorldPosition(x, height);
            Gizmos.DrawLine(start, end);
        }
        for (int y = 0; y <= height; y++)
        {
            Vector3 start = FarmToWorldPosition(0, y);
            Vector3 end = FarmToWorldPosition(width, y);
            Gizmos.DrawLine(start, end);
        }
    }
}
