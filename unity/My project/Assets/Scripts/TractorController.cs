using UnityEngine;

public class TractorController : MonoBehaviour
{
    public Vector3 targetPosition;
    public float moveSpeed = 5f;

    void Update()
    {
        if (transform.position != targetPosition)
        {
            // Move towards target position
            transform.position = Vector3.MoveTowards(transform.position, targetPosition, moveSpeed * Time.deltaTime);

            // Rotate tractor to face movement direction
            Vector3 moveDirection = (targetPosition - transform.position).normalized;
            if (moveDirection != Vector3.zero)
            {
                Quaternion targetRotation = Quaternion.LookRotation(moveDirection);
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, moveSpeed * Time.deltaTime);
            }
        }
    }
}
