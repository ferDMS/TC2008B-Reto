using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TractorVisualizer : MonoBehaviour
{
    void OnDrawGizmos()
    {
      
        Gizmos.color = Color.blue;
        Gizmos.DrawRay(transform.position, transform.forward);

        Gizmos.color = Color.yellow;
        Gizmos.DrawWireCube(transform.position, GetComponent<Collider>().bounds.size);
    }
}