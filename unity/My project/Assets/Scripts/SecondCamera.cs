using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class SecondCamera : MonoBehaviour
{
    // List of tractors to follow
    public List<Transform> tractors = new List<Transform>();
    public float distanceBehind = 5f; // Distance behind the tractor
    public float heightAbove = 2f;    // Height above the tractor
    public float followSpeed = 5f;    // Speed to follow the tractor
    public float rotationSpeed = 10f; // Speed to adjust the camera's rotation

    private int currentTractorIndex = 0;
    private bool tractorsInitialized = false;

    void Start()
    {
        StartCoroutine(InitializeTractors());
    }

    IEnumerator InitializeTractors()
    {
        // Wait until tractors are available
        while (!tractorsInitialized)
        {
            // Find all GameObjects tagged as "Tractor"
            GameObject[] tractorObjects = GameObject.FindGameObjectsWithTag("Tractor");
            if (tractorObjects.Length > 0)
            {
                tractors.Clear();
                foreach (GameObject tractorObj in tractorObjects)
                {
                    tractors.Add(tractorObj.transform);
                }

                tractorsInitialized = true;
                Debug.Log("Tractors initialized.");
            }
            else
            {
                // Wait for the next frame before checking again
                yield return null;
            }
        }
    }

    void Update()
    {
        if (!tractorsInitialized)
            return;

        // Handle input to switch between tractors
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
            Debug.LogWarning("Tractor at index " + currentTractorIndex + " is null.");
            return;
        }

        // Calculate the desired position of the camera behind the tractor
        Vector3 desiredPosition = tractor.position - tractor.forward * distanceBehind + Vector3.up * heightAbove;

        // Smoothly move the camera towards the desired position
        transform.position = Vector3.Lerp(transform.position, desiredPosition, followSpeed * Time.deltaTime);

        // Set the camera to look at the tractor (or ahead of the tractor)
        Vector3 lookAtPoint = tractor.position + tractor.forward * 5f; // Look ahead of the tractor
        Quaternion desiredRotation = Quaternion.LookRotation(lookAtPoint - transform.position);
        transform.rotation = Quaternion.Slerp(transform.rotation, desiredRotation, rotationSpeed * Time.deltaTime);
    }

    public void SwitchToNextTractor()
    {
        if (tractors.Count == 0) return;

        currentTractorIndex = (currentTractorIndex + 1) % tractors.Count;
        Debug.Log("Switched to tractor " + currentTractorIndex);
    }

    public void SwitchToPreviousTractor()
    {
        if (tractors.Count == 0) return;

        currentTractorIndex = (currentTractorIndex - 1 + tractors.Count) % tractors.Count;
        Debug.Log("Switched to tractor " + currentTractorIndex);
    }
}
