// Pathfinding.cs
using System.Collections.Generic;
using UnityEngine;

public class Pathfinding : MonoBehaviour
{
    public FarmMap farmMap;

    void Start()
    {
        if (farmMap == null)
            farmMap = FindObjectOfType<FarmMap>();
    }

    public List<Vector2Int> FindPath(Vector2Int startPos, Vector2Int targetPos)
    {
        Node startNode = new Node(startPos, farmMap.IsWalkable(startPos.x, startPos.y));
        Node targetNode = new Node(targetPos, farmMap.IsWalkable(targetPos.x, targetPos.y));

        if (!startNode.walkable || !targetNode.walkable)
            return new List<Vector2Int>(); // No path if start or end is blocked

        List<Node> openSet = new List<Node> { startNode };
        HashSet<Node> closedSet = new HashSet<Node>();

        while (openSet.Count > 0)
        {
            Node currentNode = openSet[0];
            for (int i = 1; i < openSet.Count; i++)
            {
                if (openSet[i].fCost < currentNode.fCost ||
                   (openSet[i].fCost == currentNode.fCost && openSet[i].hCost < currentNode.hCost))
                {
                    currentNode = openSet[i];
                }
            }

            openSet.Remove(currentNode);
            closedSet.Add(currentNode);

            if (currentNode.farmPosition == targetNode.farmPosition)
            {
                return RetracePath(startNode, currentNode);
            }

            foreach (Vector2Int neighborPos in GetNeighbors(currentNode.farmPosition))
            {
                if (!farmMap.IsWalkable(neighborPos.x, neighborPos.y))
                    continue;

                Node neighborNode = new Node(neighborPos, true);

                if (closedSet.Contains(neighborNode))
                    continue;

                float newMovementCostToNeighbor = currentNode.gCost + GetDistance(currentNode.farmPosition, neighborNode.farmPosition);
                if (newMovementCostToNeighbor < neighborNode.gCost || !openSet.Contains(neighborNode))
                {
                    neighborNode.gCost = newMovementCostToNeighbor;
                    neighborNode.hCost = GetDistance(neighborNode.farmPosition, targetNode.farmPosition);
                    neighborNode.parent = currentNode;

                    if (!openSet.Contains(neighborNode))
                        openSet.Add(neighborNode);
                }
            }
        }

        return new List<Vector2Int>(); // No path found
    }

    List<Vector2Int> RetracePath(Node startNode, Node endNode)
    {
        List<Vector2Int> path = new List<Vector2Int>();
        Node currentNode = endNode;

        while (currentNode.farmPosition != startNode.farmPosition)
        {
            path.Add(currentNode.farmPosition);
            currentNode = currentNode.parent;
        }
        path.Reverse();
        return path;
    }

    float GetDistance(Vector2Int a, Vector2Int b)
    {
        int dstX = Mathf.Abs(a.x - b.x);
        int dstY = Mathf.Abs(a.y - b.y);

        if (dstX > dstY)
            return 14 * dstY + 10 * (dstX - dstY);
        return 14 * dstX + 10 * (dstY - dstX);
    }

    List<Vector2Int> GetNeighbors(Vector2Int pos)
    {
        List<Vector2Int> neighbors = new List<Vector2Int>
        {
            new Vector2Int(pos.x + 1, pos.y),
            new Vector2Int(pos.x - 1, pos.y),
            new Vector2Int(pos.x, pos.y + 1),
            new Vector2Int(pos.x, pos.y - 1)
            // Add diagonals if needed
        };

        return neighbors;
    }
}
