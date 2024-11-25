using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TractorUIManager : MonoBehaviour
{
    // List of Text UI elements to display tractor info
    public List<Text> tractorTextUIList;
    public FarmController farmController;

    private int currentStep = 0;
    private float timeSinceLastStep = 0f;
    public float timeBetweenSteps = 1f; // Adjust as needed

    void Start()
    {
        if (farmController == null)
        {
            Debug.LogError("FarmController not assigned in TractorUIManager");
        }

        // Start updating the UI after the simulation is initialized
        farmController.OnSimulationInitialized.AddListener(() => UpdateTractorUI());
    }

    void Update()
    {
        if (farmController == null || farmController.stepsList == null || farmController.stepsList.Count == 0)
        {
            return;
        }

        timeSinceLastStep += Time.deltaTime;

        if (timeSinceLastStep >= timeBetweenSteps)
        {
            timeSinceLastStep = 0f;
            currentStep++;

            if (currentStep >= farmController.GetTotalSteps())
            {
                currentStep = 0; // Loop back to start or stop updating
            }

            UpdateTractorUI();
        }
    }

    void UpdateTractorUI()
    {
        StepInfo stepInfo = farmController.GetStepInfo(currentStep);
        if (stepInfo == null)
        {
            Debug.LogError($"No StepInfo found for step {currentStep}");
            return;
        }

        for (int i = 0; i < stepInfo.tractors.Count; i++)
        {
            if (i >= tractorTextUIList.Count)
            {
                Debug.LogError("Not enough Text UI elements assigned for the number of tractors");
                return;
            }

            TractorInfo tractor = stepInfo.tractors[i];
            Text tractorText = tractorTextUIList[i];

            tractorText.text = $"Tractor {i + 1}:\n" +
                               $"Task: {tractor.task}\n" +
                               $"Water: {tractor.water_level}\n" +
                               $"Fuel: {tractor.fuel_level}\n" +
                               $"Wheat: {tractor.wheat_level}";
        }
    }
}
