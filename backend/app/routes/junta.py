from flask import Blueprint, jsonify, request  # type: ignore[import]
from services.JuntaDirectivaService import JuntaDirectivaService

junta_bp = Blueprint('junta_bp', __name__)
service = JuntaDirectivaService()


@junta_bp.route('/api/junta', methods=['GET'])
def listar_miembros():
    try:
        miembros = service.listar_miembros()
        return jsonify({"status": "success", "data": miembros}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@junta_bp.route('/api/junta/<int:id_miembro>', methods=['PUT'])
def actualizar_miembro(id_miembro):
    try:
        datos = request.get_json()
        cargo = datos.get('cargo')
        url_foto = datos.get('url_foto')

        service.modificar_perfil_miembro(id_miembro, cargo, url_foto)
        return jsonify({"status": "success", "message": "Miembro actualizado correctamente"}), 200
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
