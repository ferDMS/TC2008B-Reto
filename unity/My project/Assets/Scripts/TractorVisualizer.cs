using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Add this script to the tractor prefab
public class TractorVisualizer : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // Draw tractor forward direction
        Gizmos.color = Color.blue;
        Gizmos.DrawRay(transform.position, transform.forward);
        
        // Draw tractor bounding box
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireCube(transform.position, GetComponent<Collider>().bounds.size);
    }
}