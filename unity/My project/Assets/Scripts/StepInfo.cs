using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class StepInfo
{
    public int step;
    public List<TractorInfo> tractors;

    // Constructor to create a StepInfo with multiple tractors
    public StepInfo(int stepNumber, List<TractorInfo> tractorsInfo)
    {
        step = stepNumber;
        tractors = tractorsInfo;
    }

    // Default constructor
    public StepInfo()
    {
        step = 0;
        tractors = new List<TractorInfo>();
    }

    public Vector2Int GetTractorPosition(int tractorId)
    {
        return this.tractors[tractorId].tractorPosition;
    }

    public string GetTractorTask(int tractorId)
    {
        return this.tractors[tractorId].tractorTask;
    }
}

[System.Serializable]
public class TractorInfo
{
    public Vector2Int tractorPosition { get; set; }
    public string tractorTask;
    public int waterLevel;
    public int fuelLevel;
    public int wheatLevel;

    // Constructor to create a TractorInfo from parameters
    public TractorInfo(int[] position, string task, int water, int fuel,int wheat)
    {
        tractorPosition = new Vector2Int(position[0], position[1]);
        tractorTask = task;
        waterLevel = water;
        fuelLevel = fuel;
        wheatLevel = wheat;
    }
}
