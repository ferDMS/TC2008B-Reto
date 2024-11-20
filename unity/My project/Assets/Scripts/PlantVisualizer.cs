using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Add this script to the plant prefab
public class PlantVisualizer : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // Draw plant up direction
        Gizmos.color = Color.green;
        Gizmos.DrawRay(transform.position, Vector3.up * 0.5f);
        
        // Draw plant bounding box
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireCube(transform.position, GetComponent<Collider>().bounds.size);
    }
}