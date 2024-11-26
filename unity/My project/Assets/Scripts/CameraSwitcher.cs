using UnityEngine;
using System.Collections.Generic;


public class CameraSwitcher : MonoBehaviour
{
    public List<GameObject> cameras;
    public int currentCameraIndex;
    
    void Start()
    {
        // Asegurarse de que solo la Main Camera está activa al inicio
        ActivateCamera(cameras[currentCameraIndex]);
    }

    void Update()
    {
        // Cambiar a la cámara 1 al presionar el botón "1"
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            currentCameraIndex = 0; // Actualiza el índice
            ActivateCamera(cameras[currentCameraIndex]);
        }

        // Cambiar a la cámara 2 al presionar el botón "2"
        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            currentCameraIndex = 1; // Actualiza el índice
            ActivateCamera(cameras[currentCameraIndex]);
        }

        // Cambiar a la cámara 3 al presionar el botón "3"
        if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            currentCameraIndex = 2; // Actualiza el índice
            ActivateCamera(cameras[currentCameraIndex]);
        }

        // Cambiar a la cámara 4 al presionar el botón "4"
        if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            currentCameraIndex = 3; // Actualiza el índice
            ActivateCamera(cameras[currentCameraIndex]);
        }
    }

    private void ActivateCamera(GameObject cameraToActivate)
    {
        foreach (GameObject camera in cameras)
        {
            if(camera != cameraToActivate)
            {
                camera.SetActive(false);
            }
            else
            {
                camera.SetActive(true);
            }
        }

    }
}
