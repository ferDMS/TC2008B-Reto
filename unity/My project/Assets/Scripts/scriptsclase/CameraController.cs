using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    [SerializeField] private float movementSpeed = 5f;
    [SerializeField] private float mouseSensitivity = 2f;
    
    private float rotationX;
    private float rotationY;
    
    private void Update()
    {
        // Rotacion de mouse
        rotationX -= Input.GetAxis("Mouse Y") * mouseSensitivity;
        rotationY += Input.GetAxis("Mouse X") * mouseSensitivity;
        
        rotationX = Mathf.Clamp(rotationX, -90f, 90f);
        transform.rotation = Quaternion.Euler(rotationX, rotationY, 0);
        
        //Movimiento con WASD y Flechas
        Vector3 input = new Vector3(
            Input.GetAxisRaw("Horizontal"),
            0,
            Input.GetAxisRaw("Vertical")
        );
        
        Vector3 movement = transform.right * input.x + transform.forward * input.z;
        transform.position += movement.normalized * movementSpeed * Time.deltaTime;
    }
}
