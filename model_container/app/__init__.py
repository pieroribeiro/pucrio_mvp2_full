import os
import mysql.connector
from flask import Flask, jsonify, request
from mysql.connector import Error
from typing import List

APP_PORT = os.getenv("APP_PORT", "8080")
app = Flask(__name__)

# Configurações do banco de dados
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "example_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "example_password")
DB_DATABASE = os.getenv("DB_DATABASE", "example_db")

def show_coins (records: List):
    results = []
    for coin in records:
        print(coin)
        # results.append({
        #     "id": coin.id,
        #     "symbol": coin.symbol,
        #     "name": coin.name,
        #     "value": coin.value,
        #     "type": coin.type,
        #     "created_at": coin.created_at
        # })

    return {"results": results}

cursor = None
# Conexão ao MySQL
try:
    db_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    if db_connection.is_connected():
        print("Conexão ao banco de dados MySQL estabelecida!")
    
    cursor = db_connection.cursor()
except Error as e:
    print("Erro durante a conexão ao MySQL:", e)

# Endpoint HEALTH: Retorna se o serviço está opk
@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "OK"})

# Endpoint GET: Retorna todos os itens
@app.route('/cotacoes', methods=['GET'])
def get_items():
    try: 
        cursor.execute("SELECT * FROM cotacoes")
        items = cursor.fetchall()
        if items:
            return jsonify(show_coins(items))
        else:
            return jsonify([])
    except Error as e:
        print("Erro na chamada de get_items:", e)
        return jsonify([])

# Endpoint GET: Retorna um item específico
@app.route('/cotacoes/<string:symbol>', methods=['GET'])
def get_item(symbol):
    try:
        cursor.execute("SELECT * FROM cotacoes WHERE symbol = %s", (symbol))
        item = cursor.fetchone()
        return jsonify(item)
    except Error as e:
        print("Erro na chamada de get_items:", e)
        jsonify([])

# Endpoint POST: Cria um novo item
@app.route('/cotacoes', methods=['POST'])
def create_item():
    try:
        data = request.json

        symbol = data['symbol']
        name = data['name']
        value = data['value']
        type = data['type']
        cursor.execute("INSERT INTO cotacoes (name) VALUES (%s)", (symbol,name,value,type))
        db_connection.commit()
        return jsonify({"message": "Item created successfully"})
    except:
        jsonify([])

# Endpoint PUT: Atualiza um item existente
@app.route('/cotacoes/<string:symbol>', methods=['PUT'])
def update_item(symbol):
    try:
        data = request.json

        symbol = data['symbol']
        name = data['name']
        value = data['value']
        type = data['type']
        cursor.execute("UPDATE cotacoes SET symbol = %s, name = %s, value = %s, type = %s WHERE id = %s", (symbol,name,value,type,symbol))
        db_connection.commit()
        return jsonify({"message": "Item updated successfully"})
    except:
        jsonify([])

# Endpoint DELETE: Deleta um item existente
@app.route('/cotacoes/<string:symbol>', methods=['DELETE'])
def delete_item(symbol):
    try:
        cursor.execute("DELETE FROM cotacoes WHERE symbol = %s", (symbol))
        db_connection.commit()
        return jsonify({"message": "Item deleted successfully"})
    except:
        jsonify([])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=APP_PORT)