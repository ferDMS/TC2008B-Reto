using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HarvesterController : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Bounds bounds = CalculateBounds();
        Vector3 size = bounds.size;
        Debug.Log("Object size: " + size);
    }

    Bounds CalculateBounds()
    {
        Renderer[] renderers = GetComponentsInChildren<Renderer>();
        if (renderers.Length == 0)
        {
            return new Bounds(transform.position, Vector3.zero);
        }

        Bounds bounds = renderers[0].bounds;
        for (int i = 1; i < renderers.Length; i++)
        {
            bounds.Encapsulate(renderers[i].bounds);
        }
        return bounds;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
