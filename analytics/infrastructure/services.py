from analytics.domain.entities import Metric
import requests
from iam.application.services import AuthApplicationService
import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict

class ExternalMetricServiceFacade:
    @staticmethod
    def get_metrics(metrics: list[Metric]) -> dict[int, int]:
        consumption_metrics = [m.metric_value for m in metrics if m.metric_types_id == 4]
        if not consumption_metrics:
            return {4: 0}
        average = sum(consumption_metrics) / len(consumption_metrics)
        return {4: average}

BACKEND_URL = 'https://ecoguardian-cgenhdd6dadrgbfz.brazilsouth-01.azurewebsites.net/api/v1/metric-registry'
PUSH_INTERVAL = 120  # segundos

metrics_buffer = defaultdict(list)

def add_metrics_to_buffer(device_id, metrics):
    metrics_buffer[device_id].extend(metrics)

def send_metric_registry_to_backend(device_id, metrics, api_key):
    iam_service = AuthApplicationService()
    if not iam_service.authenticate(device_id, api_key):
        raise ValueError("Autenticación fallida: device_id o api_key inválidos")
    payload = {
        "deviceId": int(device_id),
        "metrics": [
            {"metricValue": float(m.metric_value), "metricTypesId": int(m.metric_types_id)} for m in metrics
        ]
    }
    headers = {
        "Device-Id": str(device_id),
        "Api-Key": api_key
    }
    try:
        response = requests.post(BACKEND_URL, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Registro de métricas enviado al backend: {payload}")
        return response.json()
    except Exception as e:
        print(f"Error enviando registro de métricas al backend: {e}")
        raise

def get_metrics_last_2_minutes():
    now = datetime.now()
    two_minutes_ago = now - timedelta(minutes=2)
    grouped = defaultdict(list)
    for device_id, metrics in metrics_buffer.items():
        recent_metrics = [m for m in metrics if hasattr(m, 'created_at') and m.created_at >= two_minutes_ago]
        # Si no hay atributo created_at, se asume que todas son recientes
        if not recent_metrics and metrics and not hasattr(metrics[0], 'created_at'):
            recent_metrics = metrics
        if recent_metrics:
            grouped[device_id].extend(recent_metrics)
    return grouped

def push_all_metric_registries_to_backend(api_key):
    grouped_metrics = get_metrics_last_2_minutes()
    for device_id, metrics in grouped_metrics.items():
        try:
            send_metric_registry_to_backend(device_id, metrics, api_key)
            metrics_buffer[device_id] = [m for m in metrics_buffer[device_id] if m not in metrics]
        except Exception as e:
            print(f"No se pudo enviar el registro de métricas del device {device_id}: {e}")

def periodic_metrics_push(api_key):
    while True:
        push_all_metric_registries_to_backend(api_key)
        time.sleep(PUSH_INTERVAL)

def start_periodic_metrics_push(api_key):
    thread = threading.Thread(target=periodic_metrics_push, args=(api_key,), daemon=True)
    thread.start()
    return thread