from abc import ABC, abstractmethod

class IObserver(ABC):
    """Contrato para cualquier clase que desee ser notificada de un evento."""
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass

class ISubject(ABC):
    """Contrato para la clase principal que emite los eventos."""
    @abstractmethod
    def attach(self, observer: IObserver):
        pass
    
    @abstractmethod
    def detach(self, observer: IObserver):
        pass
    
    @abstractmethod
    def notify(self, event_type: str, data: dict):
        pass