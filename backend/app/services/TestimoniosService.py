from ..repositories.TestimoniosRepository import TestimoniosRepository
from ..interfaces.ITestimoniosRepository import ITestimoniosRepository


class TestimoniosService:

    def __init__(self, repository: ITestimoniosRepository = None):
        """Constructor corregido con importaciones relativas."""
        self.repository = repository if repository is not None else TestimoniosRepository()

    def obtener_testimonios_publicos(self):
        try:
            return self.repository.obtener_todos_aprobados()
        except Exception as e:
            raise e