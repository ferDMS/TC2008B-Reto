using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class OldTVEffect : MonoBehaviour
{
    public Material effectMaterial;

    private void OnRenderImage(RenderTexture src, RenderTexture dest)
    {
        if (effectMaterial != null)
        {
            Graphics.Blit(src, dest, effectMaterial);
        }
        else
        {
            Graphics.Blit(src, dest);
        }
    }
}
