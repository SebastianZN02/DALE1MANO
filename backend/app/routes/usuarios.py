from flask import Blueprint, jsonify, request
from ..db import call_sp, db_instance

usuarios_bp = Blueprint('usuarios_bp', __name__)


@usuarios_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Llamamos al procedimiento almacenado SP_BuscarUsuarios pasándole un string vacío para traer todos
        resultados = call_sp("SP_BuscarUsuarios", ("",))
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@usuarios_bp.route('/api/usuarios/<int:id_usuario>/promover', methods=['POST'])
def promover_usuario(id_usuario):
    try:
        call_sp("SP_PromoverMiembro", (id_usuario,))
        return jsonify({"status": "success", "message": "Usuario promovido a miembro oficial correctamente."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@usuarios_bp.route('/api/asistencias', methods=['GET'])
def listar_asistencias():
    conn = db_instance.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_asistencia, id_usuario, id_proyecto, fecha_inscripcion, asistio FROM Asistencias")
        resultados = cursor.fetchall()
        # Formatear la fecha a ISO string para compatibilidad JSON
        for r in resultados:
            if r.get("fecha_inscripcion"):
                r["fecha_inscripcion"] = r["fecha_inscripcion"].isoformat()
        return jsonify({"status": "success", "data": resultados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        db_instance.close_connection(conn)
