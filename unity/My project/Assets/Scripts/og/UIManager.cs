// UIManager.cs
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class UIManager : MonoBehaviour
{
    public static UIManager Instance;

    [Header("UI Elements")]
    public Text stepText;
    public Text tractorInfoText;
    public Text plantInfoText;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(gameObject);
    }

    // Updates the current simulation step
    public void UpdateStep(int currentStep, int totalSteps)
    {
        if (stepText != null)
            stepText.text = $"Step: {currentStep}/{totalSteps}";
    }

    // Updates tractor information
    public void UpdateTractorInfo(List<Tractor> tractors)
    {
        if (tractorInfoText == null)
            return;

        tractorInfoText.text = "Tractors:\n";
        foreach (var tractor in tractors)
        {
            tractorInfoText.text += $"ID: {tractor.GetInstanceID()}, Task: {tractor.CurrentTask}, Fuel: {tractor.FuelLevel}, Wheat: {tractor.WheatLevel}\n";
        }
    }

    // Updates plant information
    public void UpdatePlantInfo(List<Plant> plants)
    {
        if (plantInfoText == null)
            return;

        plantInfoText.text = "Plants:\n";
        foreach (var plant in plants)
        {
            plantInfoText.text += $"Pos: ({plant.Position.x}, {plant.Position.y}), Maturity: {plant.Maturity}, Watered: {plant.IsWatered}, Harvested: {plant.Harvested}\n";
        }
    }
}
