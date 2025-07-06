from flask import request, Blueprint, jsonify
from analytics.application.services import MetricService
from analytics.domain.entities import Metric
from analytics.infrastructure.services import ExternalMetricServiceFacade
from iam.interfaces.services import authenticate_request

metric_api = Blueprint('metric_api', __name__)

@metric_api.route('/metrics', methods=['POST'])
def calculate_average_consume():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    if not data or 'metrics' not in data or 'deviceId' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    metrics_data = data['metrics']
    device_id = data['deviceId']
    if not isinstance(metrics_data, list):
        return jsonify({'error': 'Metrics must be a list'}), 400

    metrics = []
    for item in metrics_data:
        if not all(k in item for k in ('metricValue', 'metricTypesId')):
            return jsonify({'error': 'Each metric must have metricValue and metricTypesId'}), 400
        metrics.append(Metric(
            metric_value=item['metricValue'],
            metric_types_id=item['metricTypesId'],
            device_id=device_id
        ))

    service = MetricService(ExternalMetricServiceFacade())
    report = service.get_average_consume(metrics)
    return jsonify({'report': report}), 200
