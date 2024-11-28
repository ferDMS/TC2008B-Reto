using System;
using UnityEngine;

public class CrearArte : MonoBehaviour
{
    public GameObject PrefabArte;
    int amount = 5;
    GameObject[] prefabs;

    float x, y, z;

    // Method to get coordinates of this GameObject
    public void GetCoordinates()
    {
        // Get the position of the GameObject
        Vector3 coordinates = transform.position;
        x = coordinates.x;
        y = coordinates.y;
        z = coordinates.z;
    }
    

    void Start()
    {
        GetCoordinates();
        prefabs = new GameObject[0];
        this.CreateInstances();
    }

    void CreateInstances()
    {
        for (int i = 0; i < amount; i++)
        {
            GameObject newObj = Instantiate(PrefabArte, new Vector3(x, y, z), Quaternion.Euler(0, 0, 0));
            Array.Resize(ref prefabs, prefabs.Length + 1);
            prefabs[prefabs.Length - 1] = newObj;
            x++;
            z++;
        }
    }
}