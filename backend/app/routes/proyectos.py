from flask import Blueprint, request, jsonify
from ..dependencies import get_proyecto_service
from ..db import call_sp

proyectos_bp = Blueprint("proyectos", __name__, url_prefix="/api/proyectos")


@proyectos_bp.route("", methods=["GET"], strict_slashes=False)
def obtener_proyectos():
    """
    Ruta para obtener la lista de proyectos, opcionalmente filtrada por estado.
    """
    estado = request.args.get("estado")  # Puede ser ACTIVO, PASADO o None
    proyecto_service = get_proyecto_service()
    try:
        proyectos = proyecto_service.obtener_proyectos(estado)
        return jsonify(proyectos), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al obtener proyectos", "details": str(e)}), 500


@proyectos_bp.route("", methods=["POST"], strict_slashes=False)
def crear_proyecto():
    """
    Ruta para crear un proyecto (CU-09).
    """
    data = request.get_json() or {}
    id_tematica = data.get("id_tematica")
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.crear_proyecto(id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)
        return jsonify({"status": "success", "message": "Proyecto creado exitosamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        if getattr(e, 'errno', None) == 1644:
            return jsonify({"error": e.msg if hasattr(e, 'msg') else str(e)}), 400
        return jsonify({"error": "Error al crear proyecto", "details": str(e)}), 500


@proyectos_bp.route("/<int:id_proyecto>", methods=["PUT"], strict_slashes=False)
def actualizar_proyecto(id_proyecto):
    """
    Ruta para actualizar un proyecto (CU-09).
    """
    data = request.get_json() or {}
    id_tematica = data.get("id_tematica")
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.actualizar_proyecto(id_proyecto, id_tematica, titulo, descripcion, fecha_inicio, fecha_fin)
        return jsonify({"status": "success", "message": "Proyecto actualizado exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        if getattr(e, 'errno', None) == 1644:
            return jsonify({"error": e.msg if hasattr(e, 'msg') else str(e)}), 400
        return jsonify({"error": "Error al actualizar proyecto", "details": str(e)}), 500


@proyectos_bp.route("/<int:id_proyecto>/status", methods=["PATCH"], strict_slashes=False)
def actualizar_estado(id_proyecto):
    """
    Ruta para actualizar el estado del proyecto (ACTIVO, PASADO, CANCELADO).
    """
    data = request.get_json() or {}
    estado = data.get("estado")

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.actualizar_estado(id_proyecto, estado)
        return jsonify({"status": "success", "message": "Estado del proyecto actualizado."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al actualizar estado del proyecto", "details": str(e)}), 500


@proyectos_bp.route("/inscribir", methods=["POST"], strict_slashes=False)
def inscribir_usuario():
    """
    Ruta para inscribir un voluntario en un proyecto (CU-14) con patrón Observer.
    """
    data = request.get_json() or {}
    id_usuario = data.get("id_usuario")
    id_proyecto = data.get("id_proyecto")

    proyecto_service = get_proyecto_service()
    try:
        proyecto_service.inscribir_usuario(id_usuario, id_proyecto)
        return jsonify({"status": "success", "message": "Usuario inscrito exitosamente."}), 200
    except Exception as e:
        if getattr(e, 'errno', None) == 1452:
            return jsonify({"error": "El usuario o proyecto especificado no existe."}), 400
        return jsonify({"error": str(e)}), 400


@proyectos_bp.route("/asistencia", methods=["POST"], strict_slashes=False)
def marcar_asistencia():
    """
    Ruta para marcar la asistencia de un voluntario (CU-14).
    """
    data = request.get_json() or {}
    id_usuario = data.get("id_usuario")
    id_proyecto = data.get("id_proyecto")
    asistio = data.get("asistio")

    try:
        call_sp("SP_MarcarAsistencia", (id_usuario, id_proyecto, asistio))
        return jsonify({"status": "success", "message": "Asistencia registrada exitosamente."}), 200
    except Exception as e:
        if getattr(e, 'errno', None) == 1452:
            return jsonify({"error": "El usuario o proyecto especificado no existe."}), 400
        return jsonify({"error": "Error al registrar asistencia", "details": str(e)}), 500