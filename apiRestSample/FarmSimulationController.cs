using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class FarmSimulationController : MonoBehaviour
{
    private string apiUrl = "http://localhost:5000";

    IEnumerator InitializeModel()
    {
        WWWForm form = new WWWForm();
        form.AddField("num_tractors", 5);
        form.AddField("water_capacity", 25);
        form.AddField("fuel_capacity", 120);

        using (UnityWebRequest www = UnityWebRequest.Post(apiUrl + "/initialize", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
            }
        }
    }

    IEnumerator StepModel(int steps = 1)
    {
        WWWForm form = new WWWForm();
        form.AddField("steps", steps);

        using (UnityWebRequest www = UnityWebRequest.Post(apiUrl + "/step", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
            }
        }
    }

    IEnumerator GetModelState()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(apiUrl + "/state"))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
            }
        }
    }

    void Start()
    {
        StartCoroutine(InitializeModel());
    }

    public void UpdateModel(int steps)
    {
        StartCoroutine(StepModel(steps));
    }

    public void FetchState()
    {
        StartCoroutine(GetModelState());
    }
}
