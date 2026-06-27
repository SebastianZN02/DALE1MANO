from interfaces.ITestimoniosRepository import ITestimoniosRepository
from db import db_instance

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