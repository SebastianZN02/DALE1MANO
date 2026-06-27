from flask import Blueprint, jsonify  # type: ignore[import]
from services.TestimoniosService import TestimoniosService

testimonios_bp = Blueprint('testimonios_bp', __name__)
service = TestimoniosService()


@testimonios_bp.route('/api/testimonios', methods=['GET'])
def get_testimonios_publicos():
    try:
        datos = service.obtener_testimonios_publicos()
        return jsonify({"status": "success", "data": datos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
