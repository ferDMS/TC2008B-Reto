using UnityEngine;

public class TractorController : MonoBehaviour
{
    public Vector3 targetPosition;
    public float moveSpeed = 5f;

    // Add these fields to store tractor state
    public int tractorId;                // Unique ID for the tractor
    public Vector2Int gridPosition;      // Current grid position of the tractor
    public string currentTask;           // Current task the tractor is performing

    private bool hasReachedTarget = false;

    // Declare a delegate and an event to notify when the tractor reaches its target position
    public delegate void TractorReachedTargetHandler(Vector2Int gridPosition, int tractorId, string task);
    public event TractorReachedTargetHandler OnTractorReachedTarget;

    void Update()
    {
        if (transform.position != targetPosition)
        {
            hasReachedTarget = false;

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
        else
        {
            if (!hasReachedTarget)
            {
                hasReachedTarget = true;
                // Tractor has just reached the target position
                OnReachedTargetPosition();
            }
        }
    }

    void OnReachedTargetPosition()
    {
        // Invoke the event to notify that the tractor has reached the target
        OnTractorReachedTarget?.Invoke(gridPosition, tractorId, currentTask);
    }
}
