from abc import ABC, abstractmethod

class IJuntaDirectivaRepository(ABC):
    
    @abstractmethod
    def obtener_miembros(self):
        pass

    @abstractmethod
    def actualizar_miembro(self, id_miembro: int, cargo: str, url_foto: str):
        pass