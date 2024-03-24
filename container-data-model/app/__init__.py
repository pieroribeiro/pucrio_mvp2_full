import os
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector

app = Flask(__name__)

# Configurações do Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API Documentation"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

# Configurações do banco de dados

DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_USER = os.getenv("MYSQL_USER", "example_user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "example_password")
DB_DATABASE = os.getenv("MYSQL_DATABASE", "example_db")

# Conexão ao MySQL
db_connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = db_connection.cursor()

# Endpoint GET: Retorna todos os itens
@app.route('/cotacoes', methods=['GET'])
def get_items():
    cursor.execute("SELECT * FROM cotacoes")
    items = cursor.fetchall()
    return jsonify(items)

# Endpoint GET: Retorna um item específico
@app.route('/cotacoes/<str:symbol>', methods=['GET'])
def get_item(symbol):
    cursor.execute("SELECT * FROM cotacoes WHERE symbol = %s", (symbol))
    item = cursor.fetchone()
    return jsonify(item)

# Endpoint POST: Cria um novo item
@app.route('/cotacoes', methods=['POST'])
def create_item():
    data = request.json

    symbol = data['symbol']
    name = data['name']
    value = data['value']
    type = data['type']
    cursor.execute("INSERT INTO cotacoes (name) VALUES (%s)", (symbol,name,value,type))
    db_connection.commit()
    return jsonify({"message": "Item created successfully"})

# Endpoint PUT: Atualiza um item existente
@app.route('/cotacoes/<str:symbol>', methods=['PUT'])
def update_item(symbol):
    data = request.json

    symbol = data['symbol']
    name = data['name']
    value = data['value']
    type = data['type']
    cursor.execute("UPDATE cotacoes SET symbol = %s, name = %s, value = %s, type = %s WHERE id = %s", (symbol,name,value,type,symbol))
    db_connection.commit()
    return jsonify({"message": "Item updated successfully"})

# Endpoint DELETE: Deleta um item existente
@app.route('/cotacoes/<str:symbol>', methods=['DELETE'])
def delete_item(symbol):
    cursor.execute("DELETE FROM cotacoes WHERE symbol = %s", (symbol))
    db_connection.commit()
    return jsonify({"message": "Item deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')