// GridManager.cs
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour
{
    public FarmMap farmMap;
    public FarmModel farmModel;
    
    [Header("Grid Settings")]
    public float tileSize = 2f;
    public float tileHeight = 0.2f;
    
    private Dictionary<Vector2Int, Plant> plantGrid = new Dictionary<Vector2Int, Plant>();

    void Start()
    {
        if (farmMap == null) farmMap = FindObjectOfType<FarmMap>();
        if (farmModel == null) farmModel = FindObjectOfType<FarmModel>();
        
        Initialize3DGrid();
    }

    void Initialize3DGrid()
    {
        foreach (Plant plant in farmModel.Plants)
        {
            Vector3 worldPos = GetWorldPosition(plant.Position);
            plant.transform.position = worldPos;
            plantGrid[plant.Position] = plant;
        }

        foreach (Tractor tractor in farmModel.Tractors)
        {
            Vector3 worldPos = GetWorldPosition(tractor.Position) + Vector3.up * tileHeight;
            tractor.transform.position = worldPos;
            tractor.GetComponent<Tractor3D>().Initialize(this);
        }

        // Position silo
        Vector3 siloPos = GetWorldPosition(farmModel.Silo.Position) + Vector3.up * tileHeight;
        farmModel.Silo.transform.position = siloPos;
    }

    public Vector3 GetWorldPosition(Vector2Int gridPos)
    {
        return new Vector3(gridPos.x * tileSize, 0, gridPos.y * tileSize);
    }

    public Vector2Int GetGridPosition(Vector3 worldPos)
    {
        return new Vector2Int(
            Mathf.RoundToInt(worldPos.x / tileSize),
            Mathf.RoundToInt(worldPos.z / tileSize)
        );
    }
}
