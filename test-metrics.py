import requests
import random
import time

EDGE_URL = "http://localhost:9000/metrics"
API_KEY = "b1e2c3d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e"
DEVICE_ID = 1  # Cambia según tu dispositivo

def send_metric(metric_value, metric_types_id, device_id):
    payload = {
        "deviceId": device_id,
        "metrics": [
            {
                "metricValue": metric_value,
                "metricTypesId": metric_types_id
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
        "Device-Id": str(device_id)
    }
    response = requests.post(EDGE_URL, json=payload, headers=headers)
    print(f"Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    for i in range(10):  # Envía 10 registros
        metric_value = round(random.uniform(10, 90), 2)  # Valor aleatorio entre 10 y 90
        metric_types_id = random.choice([1, 2, 3, 4])    # Tipo de métrica aleatorio
        send_metric(metric_value, metric_types_id, DEVICE_ID)
        time.sleep(1)  # Espera 1 segundo entre envíos