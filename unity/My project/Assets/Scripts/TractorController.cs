using UnityEngine;

public class TractorController : MonoBehaviour
{
    public Vector3 targetPosition;
    public float moveSpeed = 5f;

    public int tractorId;
    public Vector2Int gridPosition;
    public string currentTask;
    
    // Add resource tracking
    public int waterLevel;
    public int fuelLevel;
    public int wheatLevel;

    private bool hasReachedTarget = false;

    public delegate void TractorReachedTargetHandler(Vector2Int gridPosition, int tractorId, string task);
    public event TractorReachedTargetHandler OnTractorReachedTarget;

    void Update()
    {
        if (transform.position != targetPosition && fuelLevel > 0) // solo se mueve si tiene combustible
        {
            hasReachedTarget = false;

            // se mueve hacia la posición objetivo
            transform.position = Vector3.MoveTowards(transform.position, targetPosition, moveSpeed * Time.deltaTime);

            // se rota hacia la dirección de movimiento
            Vector3 moveDirection = (targetPosition - transform.position).normalized;
            if (moveDirection != Vector3.zero)
            {
                Quaternion targetRotation = Quaternion.LookRotation(moveDirection);
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, moveSpeed * Time.deltaTime);
            }
        }
        else if (!hasReachedTarget)
        {
            hasReachedTarget = true;
            OnReachedTargetPosition();
        }
    }

    // Update resource levels
    public void UpdateResources(int water, int fuel, int wheat)
    {
        waterLevel = water;
        fuelLevel = fuel;
        wheatLevel = wheat;
    }

    void OnReachedTargetPosition()
    {
        if (OnTractorReachedTarget != null)
        {
            OnTractorReachedTarget(gridPosition, tractorId, currentTask);
        }
    }
}