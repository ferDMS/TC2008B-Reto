// Node.cs
// Node.cs
using UnityEngine;

public class Node
{
    public Vector2Int farmPosition;
    public bool walkable;
    public float gCost; // Cost from start node
    public float hCost; // Heuristic cost to end node
    public float fCost { get { return gCost + hCost; } }
    public Node parent;

    public Node(Vector2Int farmPosition, bool walkable)
    {
        this.farmPosition = farmPosition;
        this.walkable = walkable;
    }
}
