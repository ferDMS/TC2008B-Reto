using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TractorUIManager : MonoBehaviour
{
    [Header("References")]
    public List<Text> tractorTextUIList;
    public FarmController farmController;

    [Header("Update Settings")]
    public float updateInterval = 0.1f;

    private List<TractorController> tractorControllers;
    private float timeSinceLastUpdate = 0f;
    private bool isInitialized = false;
    

    void Start()
    {
        if (farmController == null)
        {
            Debug.LogError("FarmController not assigned in TractorUIManager");
            return;
        }

        tractorControllers = new List<TractorController>();
        farmController.OnSimulationInitialized.AddListener(InitializeTractorReferences);
    }

    void InitializeTractorReferences()
    {
        Debug.Log("Initializing TractorUIManager");
        tractorControllers.Clear();
        
        // Wait one frame to ensure all tractors are created
        StartCoroutine(InitializeAfterDelay());
    }

    System.Collections.IEnumerator InitializeAfterDelay()
    {
        yield return null; // Wait one frame

        GameObject tractorsParent = GameObject.Find("Tractors");
        if (tractorsParent != null)
        {
            foreach (Transform tractorTransform in tractorsParent.transform)
            {
                TractorController controller = tractorTransform.GetComponent<TractorController>();
                if (controller != null)
                {
                    tractorControllers.Add(controller);
                    Debug.Log($"Found Tractor Controller {controller.tractorId}");
                }
            }
        }

        if (tractorControllers.Count == 0)
        {
            Debug.LogError("No tractor controllers found!");
            yield break;
        }

        if (tractorTextUIList.Count < tractorControllers.Count)
        {
            Debug.LogWarning($"Not enough UI elements ({tractorTextUIList.Count}) for all tractors ({tractorControllers.Count})");
        }

        isInitialized = true;
        UpdateTractorUI(); // Initial update
    }

    void Update()
    {
        if (!isInitialized) return;

        timeSinceLastUpdate += Time.deltaTime;
        if (timeSinceLastUpdate >= updateInterval)
        {
            UpdateTractorUI();
            timeSinceLastUpdate = 0f;
        }
    }

    void UpdateTractorUI()
    {
        if (tractorControllers == null || tractorControllers.Count == 0)
        {
            Debug.LogWarning("No tractor controllers available for UI update");
            return;
        }

        for (int i = 0; i < tractorControllers.Count && i < tractorTextUIList.Count; i++)
        {
            TractorController tractor = tractorControllers[i];
            Text tractorText = tractorTextUIList[i];

            if (tractor == null || tractorText == null) continue;

            string status = GetMovementStatus(tractor);
            Color statusColor = GetStatusColor(tractor.currentTask);

            string resourceWarnings = GetResourceWarnings(tractor);
            string colorHex = ColorUtility.ToHtmlStringRGB(statusColor);

            string uiText = $"<color=#{colorHex}>Tractor {i + 1}</color>\n" +
                           $"Status: {status}\n" +
                           $"Task: {tractor.currentTask}\n" +
                           $"Position: ({tractor.gridPosition.x}, {tractor.gridPosition.y})\n" +
                           $"Resources:\n" +
                           $"• Water: {tractor.waterLevel}{(tractor.waterLevel == 0 ? " ⚠" : "")}\n" +
                           $"• Fuel: {tractor.fuelLevel}{(tractor.fuelLevel == 0 ? " ⚠" : "")}\n" +
                           $"• Wheat: {tractor.wheatLevel}\n" +
                           (resourceWarnings != "" ? $"\n{resourceWarnings}" : "");

            tractorText.text = uiText;
        }
    }

    private string GetMovementStatus(TractorController tractor)
    {
        if (tractor.fuelLevel <= 0)
            return "Out of Fuel!";
        
        if (Vector3.Distance(tractor.transform.position, tractor.targetPosition) > 0.01f)
            return "Moving";

        switch (tractor.currentTask.ToLower())
        {
            case "watering": return "Watering";
            case "harvesting": return "Harvesting";
            case "depositing": return "Depositing";
            default: return "Idle";
        }
    }

    private string GetResourceWarnings(TractorController tractor)
    {
        List<string> warnings = new List<string>();
        
        if (tractor.fuelLevel == 0)
            warnings.Add("<color=red>Out of Fuel!</color>");
        else if (tractor.fuelLevel < 10)
            warnings.Add("<color=yellow>Low Fuel!</color>");
            
        if (tractor.waterLevel == 0)
            warnings.Add("<color=red>Out of Water!</color>");
        else if (tractor.waterLevel < 10)
            warnings.Add("<color=yellow>Low Water!</color>");
            
        return string.Join("\n", warnings);
    }

    private Color GetStatusColor(string task)
    {
        switch (task.ToLower())
        {
            case "watering":
                return new Color(0.2f, 0.6f, 1f); // Light blue
            case "harvesting":
                return new Color(0.4f, 0.8f, 0.4f); // Light green
            case "depositing":
                return new Color(1f, 0.8f, 0.2f); // Gold
            case "idle":
                return new Color(0.7f, 0.7f, 0.7f); // Gray
            default:
                return Color.white;
        }
    }

    void OnDestroy()
    {
        if (farmController != null)
        {
            farmController.OnSimulationInitialized.RemoveListener(InitializeTractorReferences);
        }
    }
}