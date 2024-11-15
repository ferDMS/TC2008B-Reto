// FarmMap.cs
using UnityEngine;

public class FarmMap : MonoBehaviour
{
    [Header("Map Dimensions")]
    public int width = 20;
    public int height = 20;
    public float cellSize = 5f;
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
                Gizmos.DrawWireCube(worldPos, Vector3.one * (cellSize - 0.1f));
            }
        }
    }
}
