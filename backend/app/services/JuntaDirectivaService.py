from ..repositories.JuntaDirectivaRepository import JuntaDirectivaRepository
from ..interfaces.IJuntaDirectivaRepository import IJuntaDirectivaRepository

class JuntaDirectivaService:

    def __init__(self, repository: IJuntaDirectivaRepository = None):
        # Si no se inyecta un repositorio, se utiliza la implementación concreta por defecto
        self.repository = repository or JuntaDirectivaRepository()

    def listar_miembros(self):
        try:
            return self.repository.obtener_miembros()
        except Exception as e:
            raise e

    def modificar_perfil_miembro(self, id_miembro: int, cargo: str, url_foto: str):
        try:
            if not cargo or not url_foto:
                raise ValueError("El cargo y la fotografía son obligatorios.")

            return self.repository.actualizar_miembro(id_miembro, cargo, url_foto)
        except Exception as e:
            raise e
