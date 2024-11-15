using UnityEngine;

public class CameraController : MonoBehaviour
{
    public float speed = 10.0f;
    public float mouseSensitivity = 200.0f; // Increased sensitivity
    private float pitch = 0.0f;
    private float yaw = 0.0f;

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        yaw = transform.eulerAngles.y;
        pitch = transform.eulerAngles.x;
    }

    void Update()
    {
        // Mouse input for looking around
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

        yaw += mouseX;
        pitch -= mouseY;
        pitch = Mathf.Clamp(pitch, -90f, 90f);

        transform.eulerAngles = new Vector3(pitch, yaw, 0.0f);

        // Keyboard input for movement
        float horizontal = Input.GetAxis("Horizontal"); // A, D
        float vertical = Input.GetAxis("Vertical"); // W, S
        float up = 0.0f;
        float down = 0.0f;

        if (Input.GetKey(KeyCode.Space))
        {
            up = 1.0f;
        }
        if (Input.GetKey(KeyCode.LeftControl))
        {
            down = 1.0f;
        }

        Vector3 direction = transform.right * horizontal + transform.up * (up - down) + transform.forward * vertical;
        transform.Translate(direction * speed * Time.deltaTime, Space.World);
    }
}
