using UnityEngine;

public class SpotlightController : MonoBehaviour
{
    private Light spotLight;
    
    void Start()
    {
      
        spotLight = GetComponent<Light>();
    
        if (spotLight != null)
            spotLight.enabled = false;
    }
    
    void Update()
    {
        
        if (Input.GetKeyDown(KeyCode.P))
        {
          
            if (spotLight != null)
                spotLight.enabled = !spotLight.enabled;
        }
    }
}