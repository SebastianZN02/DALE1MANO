from ..interfaces.IJuntaDirectivaRepository import IJuntaDirectivaRepository
from ..db import db_instance


class JuntaDirectivaRepository(IJuntaDirectivaRepository):

    def __init__(self, db_provider=db_instance):
        self.db = db_provider

    def obtener_miembros(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('SP_ObtenerJuntaDirectiva')
            resultados = next(cursor.stored_results()).fetchall()
            return resultados
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def actualizar_miembro(self, id_miembro: int, cargo: str, url_foto: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('SP_ActualizarMiembroJunta', [
                            id_miembro, cargo, url_foto])
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()