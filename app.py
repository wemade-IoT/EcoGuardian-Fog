from flask import Flask
from analytics.interfaces.services import metric_api
from analytics.infrastructure.services import start_periodic_metrics_push

app = Flask(__name__)
app.register_blueprint(metric_api)

API_KEY = 'b1e2c3d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e'

if __name__ == '__main__':
    start_periodic_metrics_push(API_KEY)
    app.run(host='0.0.0.0',port=9000, debug=True)
