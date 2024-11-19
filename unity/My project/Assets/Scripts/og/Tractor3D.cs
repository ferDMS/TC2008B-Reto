// Tractor3D.cs
[RequireComponent(typeof(Tractor))]
public class Tractor3D : MonoBehaviour
{
    private Tractor tractor;
    private GridManager gridManager;
    
    [Header("Movement")]
    public float moveSpeed = 5f;
    public float rotationSpeed = 360f;
    public float hoverHeight = 0.5f;
    
    private Queue<Vector3> pathPoints = new Queue<Vector3>();

    public void Initialize(GridManager gm)
    {
        gridManager = gm;
        tractor = GetComponent<Tractor>();
    }

    void Update()
    {
        if (pathPoints.Count > 0 && tractor.FuelLevel > 0)
        {
            Vector3 targetPos = pathPoints.Peek() + Vector3.up * hoverHeight;
            Vector3 direction = targetPos - transform.position;

            if (direction != Vector3.zero)
            {
                // Rotation
                Quaternion targetRotation = Quaternion.LookRotation(direction);
                transform.rotation = Quaternion.RotateTowards(
                    transform.rotation,
                    targetRotation,
                    rotationSpeed * Time.deltaTime
                );

                // Movement
                transform.position = Vector3.MoveTowards(
                    transform.position,
                    targetPos,
                    moveSpeed * Time.deltaTime
                );

                if (Vector3.Distance(transform.position, targetPos) < 0.1f)
                {
                    pathPoints.Dequeue();
                    tractor.Position = gridManager.GetGridPosition(targetPos);
                    tractor.ConsumeFuel();
                }
            }
        }
    }

    public void UpdatePath(List<Vector2Int> newPath)
    {
        pathPoints.Clear();
        foreach (Vector2Int gridPos in newPath)
        {
            pathPoints.Enqueue(gridManager.GetWorldPosition(gridPos));
        }
    }
}