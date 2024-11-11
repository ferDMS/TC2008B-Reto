using UnityEngine;
using UnityEngine.Networking;

public class FarmSimulationController : MonoBehaviour
{
    private string apiUrl = "http://localhost:5000";

    IEnumerator InitializeModel()
    {
        WWWForm form = new WWWForm();
        form.AddField("num_tractors", 5);
        form.AddField("water_capacity", 25);
        form.AddField("fuel_capacity", 120);
        form.AddField("steps", 300);

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

    IEnumerator StepModel()
    {
        using (UnityWebRequest www = UnityWebRequest.Post(apiUrl + "/step", ""))
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
}