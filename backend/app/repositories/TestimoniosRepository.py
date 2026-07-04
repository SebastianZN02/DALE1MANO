from ..interfaces.ITestimoniosRepository import ITestimoniosRepository
from ..db import db_instance


class TestimoniosRepository(ITestimoniosRepository):

    def __init__(self, db_provider=db_instance):
        self.db = db_provider

    def obtener_todos_aprobados(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('SP_ObtenerTestimonios')
            resultados = next(cursor.stored_results()).fetchall()
            return resultados
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT t.id_testimonio, t.id_usuario, t.id_proyecto, u.nombre_completo, p.titulo AS proyecto, t.contenido, t.url_video, t.fecha_publicacion, t.aprobado FROM Testimonios t INNER JOIN Usuarios u ON t.id_usuario = u.id_usuario INNER JOIN Proyectos p ON t.id_proyecto = p.id_proyecto ORDER BY t.fecha_publicacion DESC"
            )
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def aprobar(self, id_testimonio: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Testimonios SET aprobado = TRUE WHERE id_testimonio = %s",
                (id_testimonio,)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def eliminar(self, id_testimonio: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM Testimonios WHERE id_testimonio = %s",
                (id_testimonio,)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)

    def crear(self, id_usuario: int, id_proyecto: int, contenido: str, url_video: str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Testimonios (id_usuario, id_proyecto, contenido, url_video, aprobado) VALUES (%s, %s, %s, %s, FALSE)",
                (id_usuario, id_proyecto, contenido, url_video)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.close_connection(conn)