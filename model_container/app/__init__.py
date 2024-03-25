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

mysql_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_DATABASE
}

def connect_to_database():
    conn = mysql.connector.connect(**mysql_config)
    return conn, conn.cursor()

# Endpoint HEALTH: Retorna se o serviço está opk
@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "OK"}), 200

# Endpoint GET: Retorna todos os itens
@app.route('/cotacoes', methods=['GET'])
def get_items():
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute(f"SELECT id, symbol, name, value, type, created_at FROM cotacoes ORDER BY created_at DESC")
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": value,
                    "type": type,
                    "created_at": created_at
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_items: {str(e)}"}), 500

# Endpoint GET: Retorna um item específico
@app.route('/cotacoes/<string:symbol>', methods=['GET'])
def get_item(symbol):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE symbol = %s ORDER BY created_at DESC", (symbol,))
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": value,
                    "type": type,
                    "created_at": created_at
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Error as e:
        return jsonify({"status": "ERROR", "message": f"Error get_item: {str(e)}"}), 500

# Endpoint POST: Cria um novo item
@app.route('/cotacoes', methods=['POST'])
def create_item():
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            symbol = data['symbol']
            name = data['name']
            value = data['value']
            type = data['type']

            cursor.execute("INSERT INTO cotacoes (name) VALUES (%s, %s, %s, %s)", (symbol, name, value, type))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({'status': 'CREATED', 'id': recordId}), 201
        else:
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500            
    except:
        return jsonify({"status": "ERROR", "message": f"Error create_item: {str(e)}"}), 500

# Endpoint PUT: Atualiza um item existente
@app.route('/cotacoes/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            symbol = data['symbol']
            name = data['name']
            value = data['value']
            type = data['type']
            cursor.execute("UPDATE cotacoes SET symbol = %s, name = %s, value = %s, type = %s WHERE id = %s", (symbol, name, value, type, id))
            conn.commit()

            cursor.close()
            conn.close()
            return jsonify({"status": "UPDATED", id: id}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except:
        return jsonify({"status": "ERROR", "message": f"Error update_item: {str(e)}"}), 500

# Endpoint DELETE: Deleta um item existente
@app.route('/cotacoes/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("DELETE FROM cotacoes WHERE id = %s", (id))
            conn.commit()

            cursor.close()
            conn.close()
            return jsonify({"status": "DELETED", "id": id}), 200
        else:
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except:
        return jsonify({"status": "ERROR", "message": f"Error delete_item: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=APP_PORT)