from app import app
from app.utils.convertDatetime import convertDatetime
from app.utils.connect_to_database import connect_to_database
from flask import jsonify, request

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
                status_message = "OK"

            cursor.close()
            conn.close()

            return jsonify({"results": {"id": id}, "status": status_message, "message": None}), 200
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
