from app import app
from app.utils.convertDatetime import convertDatetime
from app.utils.connect_to_database import connect_to_database
from flask import jsonify, request

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
                value_buy: 
                    type: number
                value_sell: 
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
                value_buy: 
                    type: number
                value_sell: 
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

            cursor.execute(f"SELECT id, symbol, name, value_buy, value_sell, variation, type, created_at FROM cotacoes ORDER BY created_at DESC LIMIT 1000")
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value_buy, value_sell, variation, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value_buy": float(value_buy),
                    "value_sell": float(value_sell),
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

            cursor.execute("SELECT id, symbol, name, value_buy, value_sell, variation, type, created_at FROM cotacoes WHERE symbol = %s ORDER BY created_at ASC LIMIT 20", (symbol,))
            records = cursor.fetchall()
            results = []
            for (id, symbol, name, value_buy, value_sell, variation, type, created_at) in records:
                results.append({
                    "id": id,
                    "symbol": symbol,
                    "name": name,
                    "value_buy": float(value_buy),
                    "value_sell": float(value_sell),
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

            cursor.execute("SELECT id, symbol, name, value_buy, value_sell, variation, type, created_at FROM cotacoes WHERE id = %s LIMIT 1", (id,))
            record = cursor.fetchone()
            if record:
                result = {
                    "id": record[0],
                    "symbol": record[1],
                    "name": record[2],
                    "value_buy": float(record[3]),
                    "value_sell": float(record[4]),
                    "variation": float(record[5]),
                    "type": record[6],
                    "created_at": convertDatetime(record[7])
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
            value_buy = float(data['value_buy'])
            value_sell = float(data['value_sell'])
            variation = float(data['variation'])
            type = data['type']
            
            cursor.execute("DELETE FROM cotacoes WHERE DATE(created_at) < (NOW() - INTERVAL 1 DAY)")
            conn.commit()

            cursor.execute("INSERT INTO cotacoes (symbol, name, value_buy, value_sell, variation, type) VALUES (%s, %s, %s, %s, %s, %s)", (symbol, name, value_buy, value_sell, variation, type))
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

