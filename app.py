from flask import Flask
from analytics.interfaces.services import metric_api

app = Flask(__name__)
app.register_blueprint(metric_api)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000, debug=True)
