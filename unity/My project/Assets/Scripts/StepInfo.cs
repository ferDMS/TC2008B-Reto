using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StepInfo
{
    public int step;
    public Vector2Int tractorPosition { get; set; }
    public string tractorTask;
    public int waterLevel;
    public int fuelLevel;

    // Constructor to create a StepInfo from JSON data
    public StepInfo(int stepNumber, int[] position, string task, int water, int fuel)
    {
        step = stepNumber;
        tractorPosition = new Vector2Int(position[0], position[1]);
        tractorTask = task;
        waterLevel = water;
        fuelLevel = fuel;
    }

    // Default constructor
    public StepInfo()
    {
        step = 0;
        tractorPosition = Vector2Int.zero;
        tractorTask = "";
        waterLevel = 0;
        fuelLevel = 0;
    }
}
