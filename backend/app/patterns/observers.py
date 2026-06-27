from app.interfaces.IObserver import IObserver

class AuditLogObserver(IObserver):
    def update(self, event_type: str, data: dict):
        if event_type == "NUEVA_INSCRIPCION":
            print(f"[AUDITORÍA] Registro exitoso: Usuario ID {data['id_usuario']} inscrito en Proyecto ID {data['id_proyecto']}")

class EmailNotificationObserver(IObserver):
    def update(self, event_type: str, data: dict):
        if event_type == "NUEVA_INSCRIPCION":
            print(f"[NOTIFICACIÓN] Simulando envío de correo de confirmación al usuario ID {data['id_usuario']}...")