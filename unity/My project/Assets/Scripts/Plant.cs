// Plant.cs
using UnityEngine;

public class Plant : MonoBehaviour
{
    public Vector2Int Position;
    public bool Watered = false;
    public bool Harvested = false;
    public int Maturity = 0;

    // Call this method each simulation step to handle growth
    public void Grow()
    {
        if (Watered && !Harvested)
        {
            Maturity++;
            Watered = false; // Reset after growth
            Debug.Log($"Plant at {Position} has grown. Maturity: {Maturity}");
        }
    }

    // Determines if the plant needs watering
    public bool NeedsWater()
    {
        return !Watered && Maturity < 10; // Example condition
    }

    // Determines if the plant is ready for harvest
    public bool IsReadyForHarvest()
    {
        return Maturity >= 10 && !Harvested; // Example condition
    }
}
