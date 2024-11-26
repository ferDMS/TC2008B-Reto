using UnityEngine;

public class SpotlightController : MonoBehaviour
{
    private Light spotLight;
    
    void Start()
    {
        // Get the Light component from this GameObject
        spotLight = GetComponent<Light>();
        
        // Ensure the light is off at start (optional)
        if (spotLight != null)
            spotLight.enabled = false;
    }
    
    void Update()
    {
        // Check if S key is pressed
        if (Input.GetKeyDown(KeyCode.P))
        {
            // Toggle the spotlight
            if (spotLight != null)
                spotLight.enabled = !spotLight.enabled;
        }
    }
}