from app import app
from app.utils.convertDatetime import convertDatetime, getNow
from app.utils.connect_to_database import connect_to_database
from flask import jsonify, request

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

            return jsonify({"results": results, "status": "OK", "message": None}), 200
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
                published_at_obj = getNow()
            
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
                published_at_obj = getNow()

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
    

