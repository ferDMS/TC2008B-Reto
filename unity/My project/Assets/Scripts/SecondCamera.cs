using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class SecondCamera : MonoBehaviour
{
    public List<Transform> tractors = new List<Transform>();
    public float distanceBehind = 5f;
    public float heightAbove = 2f;
    public float followSpeed = 5f;
    public float rotationSpeed = 10f;

    private int currentTractorIndex = 0;
    private bool tractorsInitialized = false;

    void Start()
    {
        StartCoroutine(InitializeTractors());
    }

    IEnumerator InitializeTractors()
    {
        while (!tractorsInitialized)
        {
            GameObject[] tractorObjects = GameObject.FindGameObjectsWithTag("Tractor");
            if (tractorObjects.Length > 0)
            {
                tractors.Clear();
                foreach (GameObject tractorObj in tractorObjects)
                {
                    tractors.Add(tractorObj.transform);
                }

                tractorsInitialized = true;
            }
            else
            {
                yield return null;
            }
        }
    }

    void Update()
    {
        if (!tractorsInitialized)
            return;

        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            SwitchToNextTractor();
        }
        else if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            SwitchToPreviousTractor();
        }
    }

    void LateUpdate()
    {
        if (!tractorsInitialized || tractors.Count == 0)
            return;

        Transform tractor = tractors[currentTractorIndex];

        if (tractor == null)
        {
            return;
        }

        Vector3 desiredPosition = tractor.position - tractor.forward * distanceBehind + Vector3.up * heightAbove;

        transform.position = Vector3.Lerp(transform.position, desiredPosition, followSpeed * Time.deltaTime);

        Vector3 lookAtPoint = tractor.position + tractor.forward * 5f;
        Quaternion desiredRotation = Quaternion.LookRotation(lookAtPoint - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, desiredRotation, rotationSpeed * Time.deltaTime);
    }

    public void SwitchToNextTractor()
    {
        if (tractors.Count == 0) return;

        currentTractorIndex = (currentTractorIndex + 1) % tractors.Count;
    }

    public void SwitchToPreviousTractor()
    {
        if (tractors.Count == 0) return;

        currentTractorIndex = (currentTractorIndex - 1 + tractors.Count) % tractors.Count;
    }
}
