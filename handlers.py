from abc import abstractmethod, ABC
from copy import copy



class Abstract(ABC):

    @abstractmethod
    def __init__(self,*args,**kwargs):
        """Конструкто обработчика"""

    @abstractmethod
    def __call__(self,posts):
        """Основной функционал"""

    @abstractmethod
    def get(self) -> dict:
        """
        Вывод обработчика, например
        обработчика статистики
        """

    def __add__(self,obj):
        return Handlers(self,obj)

    def __raddr__(self,obj):
        return Handlers(self,obj)


class Handlers(Abstract):
    handlers = []
    def __init__(self,*args):
        for arg in args:
            if arg is None:
                continue
            elif not issubclass(arg.__class__,Abstract):
                raise TypeError("Объект может быть только наследованным от Abstract")
            elif type(arg) == Handlers:
                self.handlers.extend(arg.handlers)
            else:
                self.handlers.append(arg)

    def __call__(self,posts):
        for handler in self.handlers:
            handler(posts)

    def get(self) -> dict:
        result = {}
        for handler in handlers:
            result = result | handler.get()
        return result

class Sorted(Abstract):

    def __init__(self,reverse=False):
        self.reverse = reverse

    def __call__(self,posts):
        posts.sort(key = lambda x: x.date,reverse=self.reverse)

    def get(self) -> dict:
        return {}

class FilterSentence(Abstract):

    def __init__(self,truedict=[],falsedict=[]):
        self.dictionary1 = truedict
        self.dictionary2 = falsedict

    def __call__(self,posts):
        for i in range(len(posts)-1,-1,-1):
            for sentence in self.dictionary1:
                if sentence.lower() not in posts[i].text.lower():
                    posts.pop(i)
                    continue

            for sentence in self.dictionary2:
                if sentence.lower() in posts[i].text.lower():
                    posts.pop(i)

    def get(self) -> dict:
        return {}


