from ..interfaces.IObserver import ISubject, IObserver
from ..patterns.observers import AuditLogObserver, EmailNotificationObserver
from ..repositories.ProyectoRepository import ProyectoRepository


class ProyectoService(ISubject):
    def __init__(self, repository=None):
        """Constructor corregido y adaptado para la inyección de dependencias en Docker."""
        super().__init__()
        self._observers = []
        # Si no nos pasan un repositorio, instanciamos el predeterminado
        self.repository = repository if repository is not None else ProyectoRepository()

        self.attach(AuditLogObserver())
        self.attach(EmailNotificationObserver())

    def attach(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

    def inscribir_usuario(self, id_usuario: int, id_proyecto: int):
        try:
            resultado = self.repository.inscribir_usuario(
                id_usuario, id_proyecto)

            self.notify("NUEVA_INSCRIPCION", {
                "id_usuario": id_usuario,
                "id_proyecto": id_proyecto
            })

            return resultado
        except Exception as e:
            raise e
