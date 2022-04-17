from abc import abstractmethod, ABC
from re import search

"""
    Здесь хранятся различные обработчики(фильтры,сортировки,
    классы для сбора статистики). Для того, чтобы их использо-
    вать в объектах класса group(groups) используйте
    group.handler = Обработчик(аргументы) и запустить:
    group.start_handler()

"""

class Abstract(ABC):
    """
    Абстрактный класс(интерфейс)
    задающий методы для будущих
    обработчиков постов.
    Такие обработчики, как сортировки
    и фильтры не требуются метод
    get
    """

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

    def __radd__(self,obj):
        return Handlers(self,obj)


class Handlers(Abstract):
    """
    Класс, возникающий при
    суммировании двух обработчиков
    """

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
    """
    Сортировка. reverse=True,
    если нужно перевернуть сортировать
    в обратном порядке
    """
    _function = lambda self,x : x.date

    def __init__(self,reverse=False):
        self.reverse = reverse

    def __call__(self,posts):
        posts.sort(key=self._function, reverse=self.reverse)

    def get(self) -> dict:
        return {}

class FilterSentence(Abstract):
    """
    Фильтр постов. Если в
    тексте поста есть notindict,
    то пост удаляется или если он не имеется
    в indict
    """

    def __init__(self,indict=[],notindict=[]):
        if type(indict) == list and type(notindict) == list:
            self.dictionary1 = indict
            self.dictionary2 = notindict
        else:
            raise TypeError("FilterSentence: в конструкторе должны быть заданы списки")

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


class FilterType(Abstract):
    """
    Фильтр, который удаляет все
    посты кроме тех, у которых
    присутствует необходимый тип в
    записи. Например записи, у которых
    есть "photo" не удаляются
    """

    def __init__(self,tp):
        self.type = tp

    def __call__(self,posts):
        for i in range(len(posts)-1,-1,-1):
            delete = True
            try:
                attachments = posts[i]["attachments"]
                for attachment in attachments:
                    if attachment["type"] in self.type:
                        delete = False
                        break
            except KeyError:
                delete = False
            finally:
                if delete:
                    posts.pop(i)


    def get(self) -> dict:
        return {}

class RegularFilter(FilterSentence):
    """
    Фильтр для работы с регулярными
    выражениями
    """

    def __call__(self,posts):
        for i in range(len(posts)-1,-1,-1):
            for sentence in self.dictionary1:
                if not re.search(sentence.lower(), posts[i].text.lower()):
                    posts.pop(i)
                    continue

            for sentence in self.dictionary2:
                if re.search(sentence.lower(), posts[i].text.lower()):
                    posts.pop(i)


class LikeSort(Sorted):

    """
    Сортировка по лайкам
    записи
    """
    _function = lambda self,x : x.likes["count"]

class Ratio(Sorted):

    """
    Отношение лайков
    и публикаций
    """
    
    _function = lambda self,x : (int(x.reposts["count"])/int(x.likes["count"]))
