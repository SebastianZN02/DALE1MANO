from repositories.TestimoniosRepository import TestimoniosRepository
from interfaces.ITestimoniosRepository import ITestimoniosRepository

class TestimoniosService:
    
    def __init__(self, repository: ITestimoniosRepository = None):
        self.repository = repository or TestimoniosRepository()

    def obtener_testimonios_publicos(self):
        try:
            return self.repository.obtener_todos_aprobados()
        except Exception as e:
            raise e