from flask import request, Blueprint, jsonify
from analytics.application.services import MetricService

metric_api = Blueprint('metric_api', __name__)

@metric_api.route('/metrics', methods=['POST'])
def calculate_average_consume():
    data = request.json
    if not data or 'consumption' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    consumption = data['consumption']
    if not isinstance(consumption, list) or not all(isinstance(x, (int, float)) for x in consumption):
        return jsonify({'error': 'Consumption must be a list of numbers'}), 400

    average = MetricService.calculate_average(consumption)
    return jsonify({'average_consumption': average}), 200