// Plant.cs
using UnityEngine;

public class Plant : MonoBehaviour
{
    public Vector2Int Position { get; set; }
    public bool Harvested { get; private set; }
    public bool IsWatered { get; private set; }
    public int Maturity { get; private set; }
    
    public bool NeedsWater()
    {
        return !IsWatered && !Harvested && Maturity < 5;
    }

    public bool IsReadyForHarvest()
    {
        return Maturity >= 5 && !Harvested;
    }

    public void Water()
    {
        IsWatered = true;
    }

    public void Grow()
    {
        if (IsWatered && !Harvested && Maturity < 5)
        {
            Maturity++;
        }
    }

    public void Harvest()
    {
        Harvested = true;
    }
}
