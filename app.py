from flask import Flask
from analytics.interfaces.services import metric_api
from analytics.infrastructure.services import start_periodic_metrics_push
from iam.application.services import AuthApplicationService

app = Flask(__name__)
app.register_blueprint(metric_api)

API_KEY = 'b1e2c3d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e'
DEVICE_ID = 1

def register_device():
    auth_service = AuthApplicationService()
    auth_service.get_or_create_test_device(DEVICE_ID, API_KEY)

if __name__ == '__main__':
    register_device()
    start_periodic_metrics_push(API_KEY)
    app.run(host='0.0.0.0',port=9000, debug=True)
