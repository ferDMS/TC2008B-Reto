// BaseTractor.cs
using UnityEngine;

public abstract class BaseTractor : MonoBehaviour
{
    // Task and Position with public setters
    public TractorTask CurrentTask { get; set; }
    public Vector2Int Position { get; set; }

    // Capacities
    public int WaterCapacity = 20;
    public int FuelCapacity = 100;
    public int WheatCapacity = 5;

    // Current Levels
    public int WaterLevel { get; protected set; }
    public int FuelLevel { get; protected set; }
    public int WheatLevel { get; protected set; }

    // Initialization
    protected virtual void Start()
    {
        WaterLevel = WaterCapacity;
        FuelLevel = FuelCapacity;
        WheatLevel = 0;
        CurrentTask = TractorTask.Idle;
    }

    // Abstract methods for task execution
    public abstract void AssignTask(TractorTask task, Vector3 targetPosition);
    public abstract void PerformTask();
}
