import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger, swag_from
from datetime import datetime

APP_PORT = os.getenv("APP_PORT", "8080")
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Configurações do banco de dados
DB_HOST = os.getenv("DB_HOST", "mysql-example")
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

@app.errorhandler(404)
def endpoint_not_found(error):
    return jsonify({"message": "Endpoint not found"}), 404

# Endpoint HEALTH: Retorna se o serviço está opk
@app.route('/health', methods=['GET'])
def get_health():
    """
    Endpoint para verificação do status do serviço
    ---
    tags:
      - Admin
    responses:
        200:
            description: OK
            schema:
                id: Health
                properties:
                    status:
                        type: string
                        description: O status do serviço
    """
    return jsonify({"status": "OK"}), 200


# Endpoint GET: Retorna todos as cotações
@app.route('/cotacoes', methods=['GET'])
def get_cotacoes():
    """
    Endpoint que retorna todas as cotações
    ---
    tags:
      - Cotações
    definitions:
        Cotacao:
            type: object
            properties:
                id: 
                    type: integer
                symbol: 
                    type: string
                name: 
                    type: string
                value: 
                    type: number
                variation: 
                    type: number
                type:
                    type: string
                created_at:
                    type: string
        
        CotacaoNew:
            type: object
            properties:
                symbol: 
                    type: string
                name: 
                    type: string
                value: 
                    type: number
                variation: 
                    type: number
                type:
                    type: string

        CotacaoReturnUnique:
            type: object
            properties:
                results: 
                    type: object
                status:
                    type: string
                message:
                    type: string

        Cotacoes:
            type: object
            properties:
                results: 
                    type: array
                    items:
                        $ref: '#/definitions/Cotacao'
                status:
                    type: string
                message:
                    type: string

        CotacoesError:
            type: object
            properties:
                results: 
                    type: string
                status:
                    type: string
                message:
                    type: string

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/Cotacoes'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("DELETE FROM cotacoes WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
            conn.commit()

            cursor.execute(f"SELECT id, symbol, name, value, variation, type, created_at FROM cotacoes ORDER BY created_at DESC LIMIT 1000")
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, variation, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": float(value),
                    "variation": float(variation),
                    "type": type,
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({"results": results, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_items: {str(e)}"}), 500


# Endpoint GET: Retorna items filtrados pelo símbolo
@app.route('/cotacoes/<string:symbol>', methods=['GET'])
def get_cotacoes_by_symbol(symbol):
    """
    Endpoint que retorna todas as cotações
    ---
    tags:
      - Cotações
    parameters:
      - name: symbol
        in: path
        type: string
        enum: ["BTC","ETH","ARS","USD","EUR","CAD","GBP"]
        required: true
        default: USD

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/Cotacoes'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("DELETE FROM cotacoes WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
            conn.commit()

            cursor.execute("SELECT id, symbol, name, value, variation, type, created_at FROM cotacoes WHERE symbol = %s ORDER BY created_at ASC LIMIT 20", (symbol,))
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value, variation, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value": float(value),
                    "variation": float(variation),
                    "type": type,
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({'results': results, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_item: {str(e)}"}), 500
    

# Endpoint GET: Retorna item específico pelo ID
@app.route('/cotacoes/<int:id>', methods=['GET'])
def get_cotacoes_by_id(id):
    """
    Endpoint que retorna a cotação pelo ID
    ---
    tags:
      - Cotações
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        default: 1

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/CotacaoReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("DELETE FROM cotacoes WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
            conn.commit()

            cursor.execute("SELECT id, symbol, name, value, variation, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0],
                    "symbol": record[1],
                    "name": record[2],
                    "value": float(record[3]),
                    "variation": float(record[4]),
                    "type": record[5],
                    "created_at": convertDatetime(record[6])
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({"results": result, "status": "ERROR", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_item: {str(e)}"}), 500
    

# Endpoint POST: Cria um novo item
@app.route('/cotacoes', methods=['POST'])
def create_cotacao():
    """
    Endpoint que cria uma cotação
    ---
    tags:
      - Cotações
    parameters:
      - name: body
        in: body
        type: integer
        required: true
        schema:
            $ref: '#/definitions/CotacaoNew'

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/CotacaoReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            symbol = data['symbol']
            name = data['name']
            value = float(data['value'])
            variation = float(data['variation'])
            type = data['type']
            
            cursor.execute("DELETE FROM cotacoes WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
            conn.commit()

            cursor.execute("INSERT INTO cotacoes (symbol, name, value, variation, type) VALUES (%s, %s, %s, %s, %s)", (symbol, name, value, variation, type))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({"results": {"id": recordId}, "status": "CREATED", "message": None}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500            
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error create_item: {str(e)}"}), 500


# Endpoint PUT: Atualiza um item existente
@app.route('/cotacoes/<int:id>', methods=['PUT'])
def update_cotacao(id):
    """
    Endpoint que atualiza uma cotação
    ---
    tags:
      - Cotações
    parameters:
      - name: body
        in: body
        type: object
        required: true
        schema:
            $ref: '#/definitions/CotacaoNew'
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/CotacaoReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            symbol = data['symbol']
            name = data['name']
            value = data['value']
            variation = data['variation']
            type = data['type']

            cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            actual_record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if actual_record:
                cursor.execute("UPDATE cotacoes SET symbol = %s, name = %s, value = %s, variation = %s, type = %s WHERE id = %s LIMIT 1", (symbol, name, value, variation, type, id))
                conn.commit()
                cursor.execute("SELECT id, symbol, name, value, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
                new_record = cursor.fetchone()
                status_message = "UPDATED"
            else:
                new_record = {}

            cursor.close()
            conn.close()
            return jsonify({"results": new_record, "status": status_message, "message": None}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error update_item: {str(e)}"}), 500


# Endpoint DELETE: Deleta um item existente
@app.route('/cotacoes/<int:id>', methods=['DELETE'])
def delete_cotacao(id):
    """
    Endpoint que exclui uma cotação
    ---
    tags:
      - Cotações
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/CotacaoReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/CotacoesError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT NULL FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if record:
                cursor.execute("DELETE FROM cotacoes WHERE id = %s LIMIT 1", (id,))
                conn.commit()
                status_message = 'DELETED'

            cursor.close()
            conn.close()
            return jsonify({"results": {"id": id}, "status": status_message, "message": None}), 204
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error delete_item: {str(e)}"}), 500









# Endpoint GET: Retorna todas as notícias
@app.route('/news', methods=['GET'])
def get_news():
    
    """
    Endpoint que retorna todas as cotações
    ---
    tags:
      - Notícias
    definitions:
        Noticia:
            type: object
            properties:
                id: 
                    type: integer
                title: 
                    type: string
                media: 
                    type: string
                url: 
                    type: string
                published_at:
                    type: string
                created_at:
                    type: string
        
        NoticiaNew:
            type: object
            properties:
                title: 
                    type: string
                media: 
                    type: string
                url: 
                    type: string
                published_at:
                    type: string

        NoticiaReturnUnique:
            type: object
            properties:
                results: 
                    type: object
                status:
                    type: string
                message:
                    type: string

        Noticias:
            type: object
            properties:
                results: 
                    type: array
                    items:
                        $ref: '#/definitions/Noticia'
                status:
                    type: string
                message:
                    type: string

        NoticiasError:
            type: object
            properties:
                results: 
                    type: string
                status:
                    type: string
                message:
                    type: string

        NoticiasErrorAlreadyExists:
            type: object
            properties:
                results: 
                    type: object
                    properties:
                        id:
                            type: integer
                status:
                    type: string
                message:
                    type: string

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/Noticias'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/NoticiasError'
    """
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():            
            cursor.execute("DELETE FROM news WHERE DATE(created_at) < (NOW() - INTERVAL 2 DAY)")
            conn.commit()

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
    """
    Endpoint que retorna a notícia pelo ID
    ---
    tags:
      - Notícias
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        default: 1

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/NoticiaReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/NoticiasError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("DELETE FROM news WHERE DATE(created_at) < (NOW() - INTERVAL 2 DAY)")
            conn.commit()

            cursor.execute("SELECT id, title, url, media, published_at, created_at FROM news WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0],
                    "title": record[1],
                    "url": record[2],
                    "media": record[3],
                    "published_at": convertDatetime(record[4]),
                    "created_at": convertDatetime(record[5])
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({"results": result, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_news_by_id: {str(e)}"}), 500


# Endpoint POST: Cria uma nova notícia
@app.route('/news', methods=['POST'])
def create_news():
    """
    Endpoint que cria uma notícia
    ---
    tags:
      - Notícias
    parameters:
      - name: body
        in: body
        type: integer
        required: true
        schema:
            $ref: '#/definitions/NoticiaNew'

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/NoticiaReturnUnique'
        409: 
            description: Registro já existe
            schema:
                $ref: '#/definitions/NoticiasErrorAlreadyExists'            
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/NoticiasError'
    """
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
            
            cursor.execute("SELECT id FROM news WHERE url = %s LIMIT 1", (url,))
            existsRecord = cursor.fetchone()
            if existsRecord:
                return jsonify({"results": {"id": existsRecord[0]}, "status": "ERROR", "message": "Record already exists"}), 409
            else:

                cursor.execute("DELETE FROM news WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
                conn.commit()

                cursor.execute("INSERT INTO news (title, url, media, published_at) VALUES (%s, %s, %s, %s)", (title, url, media, published_at_obj))
                conn.commit()
                recordId = cursor.lastrowid

                cursor.close()
                conn.close()

                return jsonify({"results": {"id": recordId}, "status": "CREATED", "message": None}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error create_news: {str(e)}"}), 500


# Endpoint PUT: Atualiza uma notícia existente
@app.route('/news/<int:id>', methods=['PUT'])
def update_news(id):
    """
    Endpoint que atualiza uma notícia
    ---
    tags:
      - Notícias
    parameters:
      - name: body
        in: body
        type: object
        required: true
        schema:
            $ref: '#/definitions/NoticiaNew'
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/NoticiaReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/NoticiasError'
    """
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
            else:
                new_record = {}

            cursor.close()
            conn.close()
            return jsonify({"results": new_record, "status": status_message, "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error update_news: {str(e)}"}), 500


# Endpoint DELETE: Deleta um item existente
@app.route('/news/<int:id>', methods=['DELETE'])
def delete_news(id):
    """
    Endpoint que exclui uma notícia
    ---
    tags:
      - Notícias
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/NoticiaReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/NoticiasError'
    """
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
            return jsonify({"results": {"id": id}, "status": status_message, "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error delete_news: {str(e)}"}), 500
    








# Endpoint GET: Retorna todas as apis ativas cadastradas
@app.route('/api', methods=['GET'])
def get_apis():
    
    """
    Endpoint que retorna todas as APIs
    ---
    tags:
      - APIs
    definitions:
        API:
            type: object
            properties:
                id: 
                    type: integer
                name: 
                    type: string
                symbol: 
                    type: string
                symbol: 
                    type: string
                url: 
                    type: string
                api_key: 
                    type: string
                load_symbols: 
                    type: string
                active: 
                    type: integer
                created_at:
                    type: string
        
        APINew:
            type: object
            properties:
                name: 
                    type: string
                symbol: 
                    type: string
                symbol: 
                    type: string
                url: 
                    type: string
                api_key: 
                    type: string
                load_symbols: 
                    type: string
                active: 
                    type: integer

        APIReturnUnique:
            type: object
            properties:
                results: 
                    type: object
                status:
                    type: string
                message:
                    type: string

        APIS:
            type: object
            properties:
                results: 
                    type: array
                    items:
                        $ref: '#/definitions/Noticia'
                status:
                    type: string
                message:
                    type: string

        APISError:
            type: object
            properties:
                results: 
                    type: string
                status:
                    type: string
                message:
                    type: string

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/APIS'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try: 
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute(f"SELECT id, name, symbol, url, api_key, load_symbols, active, created_at FROM apis WHERE active = 1 ORDER BY created_at DESC LIMIT 10")
            records = cursor.fetchall()
            results = []
            for (id, name, symbol, url, api_key, load_symbols, active, created_at) in records:
                results.append({
                    "id": id, 
                    "name": name, 
                    "symbol": symbol, 
                    "url": url, 
                    "api_key": api_key, 
                    "load_symbols": load_symbols,
                    "active": active, 
                    "created_at": convertDatetime(created_at)
                })

            cursor.close()
            conn.close()

            return jsonify({"results": results, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_apis: {str(e)}"}), 500


# Endpoint GET: Retorna uma api específica pelo SYMBOL
@app.route('/api/<string:symbol>', methods=['GET'])
def get_api_by_symbol(symbol):
    """
    Endpoint que retorna as APIs pelo símbolo
    ---
    tags:
      - APIs
    parameters:
      - name: symbol
        in: path
        type: string
        enum: ["coin","crypto"]
        required: true
        default: crypto

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/APIS'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, name, symbol, url, api_key, load_symbols, active, created_at FROM apis WHERE symbol = %s LIMIT 1", (symbol,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0], 
                    "name": record[1], 
                    "symbol": record[2], 
                    "url": record[3], 
                    "api_key": record[4], 
                    "load_symbols": record[5], 
                    "active": record[6], 
                    "created_at": convertDatetime(record[7])
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({"results": result, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_api_by_symbol: {str(e)}"}), 500


# Endpoint GET: Retorna uma api específica pelo ID
@app.route('/api/<int:id>', methods=['GET'])
def get_api_by_id(id):
    """
    Endpoint que retorna a API pelo ID
    ---
    tags:
      - APIs
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        default: 1

    responses:
        200:
            description: OK
            schema:
                $ref: '#/definitions/APIReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT id, name, symbol, url, api_key, load_symbols, active, created_at FROM apis WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0], 
                    "name": record[1], 
                    "symbol": record[2], 
                    "url": record[3], 
                    "api_key": record[4], 
                    "load_symbols": record[5], 
                    "active": record[6], 
                    "created_at": convertDatetime(record[7])
                }
            else:
                result = {}

            cursor.close()
            conn.close()

            return jsonify({"results": result, "status": "OK", "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error get_api_by_id: {str(e)}"}), 500


# Endpoint POST: Cria uma nova api
@app.route('/api', methods=['POST'])
def create_api():
    """
    Endpoint que cria uma API
    ---
    tags:
      - APIs
    parameters:
      - name: body
        in: body
        type: integer
        required: true
        schema:
            $ref: '#/definitions/APINew'

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/APIReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            name = data['name']
            symbol = data['symbol']
            url = data['url']
            api_key = data['api_key']
            active = data['active']
            load_symbols = data['load_symbols']

            cursor.execute("INSERT INTO apis (name, symbol, url, api_key, load_symbols, active) VALUES (%s, %s, %s, %s, %s, %s)", (name, symbol, url, api_key, load_symbols, active))
            conn.commit()

            recordId = cursor.lastrowid

            cursor.close()
            conn.close()

            return jsonify({"results": {"id": recordId}, "status": "CREATED", "message": None}), 201
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error create_api: {str(e)}"}), 500


# Endpoint PUT: Atualiza uma api existente
@app.route('/api/<int:id>', methods=['PUT'])
def update_api(id):
    """
    Endpoint que atualiza uma API
    ---
    tags:
      - APIs
    parameters:
      - name: body
        in: body
        type: object
        required: true
        schema:
            $ref: '#/definitions/APINew'
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/APIReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            data = request.json

            name = data['name']
            symbol = data['symbol']
            url = data['url']
            api_key = data['api_key']
            load_symbols = data['load_symbols']            
            active = data['active']            

            cursor.execute("SELECT NULL FROM apis WHERE id = %s LIMIT 1", (id,))
            actual_record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if actual_record:
                cursor.execute("UPDATE apis SET name = %s, symbol = %s, url = %s, api_key = %s, load_symbols = %s, active = %s WHERE id = %s LIMIT 1", (name, symbol, url, api_key, load_symbols, active, id))
                conn.commit()
                cursor.execute("SELECT id, name, symbol, url, api_key, load_symbols, active, created_at FROM apis WHERE id = %s LIMIT 1", (id,))
                new_record = cursor.fetchone()
                status_message = "OK"
            else:
                new_record = []

            cursor.close()
            conn.close()

            if len(new_record) > 0:
                return jsonify({"results": new_record, "status": status_message, "message": None}), 200
            else:
                return jsonify({"results": None, "status": status_message, "message": None, "id": id, "new-record": {}}), 404
        else:
            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500  
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error update_api: {str(e)}"}), 500


# Endpoint DELETE: Deleta uma api existente
@app.route('/api/<int:id>', methods=['DELETE'])
def delete_api(id):
    """
    Endpoint que exclui uma API
    ---
    tags:
      - APIs
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
        201:
            description: OK
            schema:
                $ref: '#/definitions/APIReturnUnique'
        500:
            description: Ocorreu um erro
            schema:
                $ref: '#/definitions/APISError'
    """
    try:
        conn, cursor = connect_to_database()
        if conn.is_connected():
            cursor.execute("SELECT NULL FROM apis WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            status_message = 'NOT_FOUND'
            if record:
                cursor.execute("DELETE FROM apis WHERE id = %s LIMIT 1", (id,))
                conn.commit()
                status_message = 'OK'

            cursor.close()
            conn.close()
            return jsonify({"results": {"id": id}, "status": status_message, "message": None}), 200
        else:

            cursor.close()
            conn.close()
            return jsonify({"results": None, "status": "ERROR", "message": "Conexão ao MySQL não estabelecida"}), 500
    except Exception as e:
        return jsonify({"results": None, "status": "ERROR", "message": f"Error delete_api: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=APP_PORT)