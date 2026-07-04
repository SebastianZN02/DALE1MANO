from abc import ABC, abstractmethod

class ITestimoniosRepository(ABC):
    
    @abstractmethod
    def obtener_todos_aprobados(self):
        pass