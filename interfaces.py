from abc import abstractmethod, ABC

class Abstract(ABC):

    @abstractmethod
    def __init__(self,*args,**kwargs):
        """Конструкто обработчика"""

    @abstractmethod
    def __call__(self,posts):
        """Основной функционал"""

    @abstractmethod(self):
    def get(self) -> dict:
        """
        Вывод обработчика, например
        обработчика статистики
        """
