using System;
using System.Collections.Generic;
using UnityEngine;

public class CreateGrass : MonoBehaviour
{
    public List<GameObject> short_grass = new List<GameObject>(4);
    public List<GameObject> tall_grass = new List<GameObject>(3);
    // int amount = 10;
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
        System.Random rand = new System.Random();
        for (float i = -30; i <= 30; i += 0.5f)
        {
            for (float j = -30; j <= 30; j += 0.5f)
            {
                if (rand.NextDouble() <= 0.8) // 80% chance to generate grass
                {
                    GameObject selectedGrass;
                    if (rand.NextDouble() <= 0.8) // 80% chance for short grass
                    {
                        selectedGrass = short_grass[rand.Next(short_grass.Count)];
                    }
                    else // 20% chance for tall grass
                    {
                        selectedGrass = tall_grass[rand.Next(tall_grass.Count)];
                    }
                    float randomYRotation = (float)(rand.NextDouble() * 360); // Random rotation around y-axis
                    GameObject newObj = Instantiate(selectedGrass, new Vector3(i, 0f, j), Quaternion.Euler(0, randomYRotation, 0));
                    Array.Resize(ref prefabs, prefabs.Length + 1);
                    prefabs[prefabs.Length - 1] = newObj;
                }
            }
        }
    }
}