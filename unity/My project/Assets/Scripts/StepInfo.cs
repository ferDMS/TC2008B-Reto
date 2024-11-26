using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StepInfo
{
    public int step;
    public List<TractorInfo> tractors;

    // Methods to access tractor info (optional)
    public Vector2Int GetTractorPosition(int tractorId)
    {
        return this.tractors[tractorId].tractorPosition;
    }

    public string GetTractorTask(int tractorId)
    {
        return this.tractors[tractorId].task;
    }
}


[System.Serializable]
public class TractorInfo
{
    public int[] position;
    public string task;
    public int water_level;
    public int fuel_level;
    public int wheat_level;

    // This property doesn't need to be serialized, so it's fine to keep it as a property
    public Vector2Int tractorPosition => new Vector2Int(position[0], position[1]);

    // Constructor (optional if you don't use it)
    public TractorInfo(int[] position, string task, int water, int fuel, int wheat)
    {
        this.position = position;
        this.task = task;
        this.water_level = water;
        this.fuel_level = fuel;
        this.wheat_level = wheat;
    }
}

