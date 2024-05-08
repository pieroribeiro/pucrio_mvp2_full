from app import app
from flask import jsonify

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