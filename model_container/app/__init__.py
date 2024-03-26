import os
import mysql.connector
from flask import Flask, jsonify, request
from typing import List
from datetime import datetime

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

def convertDatetime(dt, isISO = True, format = '%Y-%m-%d %H:%M:%S'):
    if isISO:
        return datetime.strptime(str(dt), format).isoformat()
    else:
        return datetime.strptime(str(dt), format)        


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
            cursor.execute(f"SELECT id, symbol, name, value, type, created_at FROM cotacoes ORDER BY created_at DESC LIMIT 1000")
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": float(value),
                    "type": type,
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_items: {str(e)}"}), 500


# Endpoint GET: Retorna items filtrados pelo símbolo
@app.route('/cotacoes/<string:symbol>', methods=['GET'])
def get_items_by_symbol(symbol):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE symbol = %s ORDER BY created_at DESC LIMIT 1000", (symbol,))
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": float(value),
                    "type": type,
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_item: {str(e)}"}), 500
    

# Endpoint GET: Retorna item específico pelo ID
@app.route('/cotacoes/<int:id>', methods=['GET'])
def get_item_by_id(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": float(value),
                    "type": type,
                    "created_at": convertDatetime(created_at)
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({'result': result}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
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
            value = float(data['value'])
            type = data['type']

            cursor.execute("INSERT INTO cotacoes (symbol, name, value, type) VALUES (%s, %s, %s, %s)", (symbol, name, value, type))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({'status': 'CREATED', 'id': recordId}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500            
    except Exception as e:
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

            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            actual_record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if actual_record:
                cursor.execute("UPDATE cotacoes SET symbol = %s, name = %s, value = %s, type = %s WHERE id = %s LIMIT 1", (symbol, name, value, type, id))
                conn.commit()
                cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
                new_record = cursor.fetchone()
                status_message = "UPDATED"

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id, "new-record": {"id": new_record[0], "symbol": new_record[1], "name": new_record[2], "value": new_record[3], "type": new_record[4], "created_at": new_record[5]}}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error update_item: {str(e)}"}), 500


# Endpoint DELETE: Deleta um item existente
@app.route('/cotacoes/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if record:
                cursor.execute("DELETE FROM cotacoes WHERE id = %s LIMIT 1", (id,))
                conn.commit()
                status_message = 'DELETED'

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error delete_item: {str(e)}"}), 500









# Endpoint GET: Retorna todas as notícias
@app.route('/news', methods=['GET'])
def get_news():
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute(f"SELECT id, title, url, media, published_at, created_at FROM news ORDER BY created_at DESC LIMIT 10")
            records = cursor.fetchall()
            results = []
            for (id, title, url, media, published_at, created_at) in records:
                results.append({
                    "id": id,
                    "title": title,
                    "url": url,
                    "media": media,
                    "published_at": convertDatetime(published_at),
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_news: {str(e)}"}), 500


# Endpoint GET: Retorna uma notícia específica pelo ID
@app.route('/news/<int:id>', methods=['GET'])
def get_news_by_id(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, title, url, media, published_at, created_at FROM news WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": id,
                    "title": title,
                    "url": url,
                    "media": media,
                    "published_at": convertDatetime(published_at),
                    "created_at": convertDatetime(created_at)
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({'result': result}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_news_by_id: {str(e)}"}), 500


# Endpoint POST: Cria uma nova notícia
@app.route('/news', methods=['POST'])
def create_news():
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            title = data['title']
            url = data['url']
            media = data['media']
            published_at = data['published_at']
            if published_at:
                published_at_obj = convertDatetime(data['published_at'], False, '%Y-%m-%dT%H:%M:%S')
            else:
                published_at_obj = datetime.now()

            cursor.execute("INSERT INTO news (title, url, media, published_at) VALUES (%s, %s, %s, %s)", (title, url, media, published_at_obj))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({'status': 'CREATED', 'id': recordId}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error create_news: {str(e)}"}), 500


# Endpoint PUT: Atualiza uma notícia existente
@app.route('/news/<int:id>', methods=['PUT'])
def update_news(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            title = data['title']
            url = data['url']
            media = data['media']
            
            published_at = data['published_at']
            if published_at:
                published_at_obj = convertDatetime(data['published_at'], False, '%Y-%m-%dT%H:%M:%S')
            else:
                published_at_obj = datetime.now()

            cursor.execute("SELECT NULL FROM news WHERE id = %s LIMIT 1", (id,))
            actual_record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if actual_record:
                cursor.execute("UPDATE news SET title = %s, url = %s, media = %s, published_at = %s WHERE id = %s LIMIT 1", (title, url, media, published_at_obj, id))
                conn.commit()
                cursor.execute("SELECT id, title, url, media, published_at, created_at FROM news WHERE id = %s LIMIT 1", (id,))
                new_record = cursor.fetchone()
                status_message = "UPDATED"

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id, "new-record": {"id": new_record[0], "title": new_record[1], "url": new_record[2], "media": new_record[3], "published_at": new_record[4], "created_at": new_record[5]}}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error update_news: {str(e)}"}), 500


# Endpoint DELETE: Deleta um item existente
@app.route('/news/<int:id>', methods=['DELETE'])
def delete_news(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT NULL FROM news WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if record:
                cursor.execute("DELETE FROM news WHERE id = %s LIMIT 1", (id,))
                conn.commit()
                status_message = 'DELETED'

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error delete_news: {str(e)}"}), 500
    








# Endpoint GET: Retorna todas as apis ativas cadastradas
@app.route('/api', methods=['GET'])
def get_apis():
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute(f"SELECT id, name, symbol, url, api_key, active, created_at FROM apis WHERE active = 1 ORDER BY created_at DESC LIMIT 10")
            records = cursor.fetchall()
            results = []
            for (id, name, symbol, url, api_key, active, created_at) in records:
                results.append({
                    "id": id, 
                    "name": name, 
                    "symbol": symbol, 
                    "url": url, 
                    "api_key": api_key, 
                    "active": active, 
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_apis: {str(e)}"}), 500


# Endpoint GET: Retorna uma api específica pelo SYMBOL
@app.route('/api/<str:symbol>', methods=['GET'])
def get_api_by_id(symbol):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, name, symbol, url, api_key, active, created_at FROM apis WHERE symbol = %s LIMIT 1", (symbol,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0], 
                    "name": record[1], 
                    "symbol": record[2], 
                    "url": record[3], 
                    "api_key": record[4], 
                    "active": record[5], 
                    "created_at": convertDatetime(record[6])
                }

            cursor.close()
            conn.close()

            return jsonify({'result': result}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_api_by_id: {str(e)}"}), 500


# Endpoint GET: Retorna uma api específica pelo ID
@app.route('/api/<int:id>', methods=['GET'])
def get_api_by_id(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, name, symbol, url, api_key, active, created_at FROM apis WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0], 
                    "name": record[1], 
                    "symbol": record[2], 
                    "url": record[3], 
                    "api_key": record[4], 
                    "active": record[5], 
                    "created_at": convertDatetime(record[6])
                }

            cursor.close()
            conn.close()

            return jsonify({'result': result}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error get_api_by_id: {str(e)}"}), 500


# Endpoint POST: Cria uma nova api
@app.route('/api', methods=['POST'])
def create_api():
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            name = data['name']
            symbol = data['symbol']
            url = data['url']
            api_key = data['api_key']
            active = data['active']

            cursor.execute("INSERT INTO apis (name, symbol, url, api_key, active) VALUES (%s, %s, %s, %s)", (name, symbol, url, api_key, active))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({'status': 'CREATED', 'id': recordId}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error create_api: {str(e)}"}), 500


# Endpoint PUT: Atualiza uma api existente
@app.route('/api/<int:id>', methods=['PUT'])
def update_api(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            name = data['name']
            symbol = data['symbol']
            url = data['url']
            api_key = data['api_key']
            active = data['active']            

            cursor.execute("SELECT NULL FROM apis WHERE id = %s LIMIT 1", (id,))
            actual_record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if actual_record:
                cursor.execute("UPDATE apis SET name = %s, symbol = %s, url = %s, api_key = %s, active = %s WHERE id = %s LIMIT 1", (name, symbol, url, api_key, active, id))
                conn.commit()
                cursor.execute("SELECT id, name, symbol, url, api_key, active, created_at FROM apis WHERE id = %s LIMIT 1", (id,))
                new_record = cursor.fetchone()
                status_message = "UPDATED"

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id, "new-record": {"id": new_record[0], "name": new_record[1], "symbol": new_record[2], "url": new_record[3], "api_key": new_record[4], "active": new_record[5], "created_at": new_record[6]}}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error update_api: {str(e)}"}), 500


# Endpoint DELETE: Deleta uma api existente
@app.route('/api/<int:id>', methods=['DELETE'])
def delete_api(id):
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT NULL FROM apis WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if record:
                cursor.execute("DELETE FROM apis WHERE id = %s LIMIT 1", (id,))
                conn.commit()
                status_message = 'DELETED'

            cursor.close()
            conn.close()
            return jsonify({"status": status_message, "id": id}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Error delete_api: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=APP_PORT)