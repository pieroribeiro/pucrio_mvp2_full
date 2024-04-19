from app.utils.get_env import get_env
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

from app.routes import handle_404, health, currencies, news, apis

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=get_env("APP_PORT", "8080"))