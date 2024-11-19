// Silo.cs
using UnityEngine;

public class Silo : MonoBehaviour
{
    public Vector2Int Position;
    public int TotalWheat = 0;

    // Method to deposit wheat
    public void DepositWheat(int amount)
    {
        TotalWheat += amount;
        Debug.Log($"Silo at {Position} now has {TotalWheat} wheat.");
    }
}
