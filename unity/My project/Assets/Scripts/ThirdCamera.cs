using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class ThirdCamera : MonoBehaviour
{
    public Transform tractor;       // Asigna el Transform del tractor en el inspector
    public float height = 10f;      // Altura de la cámara sobre el tractor
    public float followSpeed = 5f;  // Velocidad de seguimiento
    public Material blurMaterial;   // Asigna el material con el shader de desenfoque
    [Range(0.0f, 10.0f)]
    public float blurAmount = 1.0f; // Ajusta la intensidad del desenfoque en el inspector

    void LateUpdate()
    {
        if (tractor == null)
        {
            Debug.LogWarning("No tractor assigned to ThirdCamera script.");
            return;
        }

        // Posicionar la cámara directamente encima del tractor
        Vector3 targetPosition = new Vector3(tractor.position.x, tractor.position.y + height, tractor.position.z);
        transform.position = Vector3.Lerp(transform.position, targetPosition, followSpeed * Time.deltaTime);

        // Apuntar hacia el tractor (opcional)
        transform.LookAt(tractor);
    }

    private void OnRenderImage(RenderTexture src, RenderTexture dest)
    {
        if (blurMaterial != null)
        {
            blurMaterial.SetFloat("_BlurSize", blurAmount);
            Graphics.Blit(src, dest, blurMaterial);
        }
        else
        {
            Graphics.Blit(src, dest);
        }
    }
}
