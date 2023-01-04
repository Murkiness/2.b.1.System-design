from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


# АТД ParentQueue
class ParentQueue(ABC, Generic[T]):

    # Конструктор
    # постусловие: создана пустая очередь
    def __init__(self) -> None: ...

    # Команды:
    # постусловие: новый элемент добавлен в конец очереди
    @abstractmethod
    def add_tail(self, value: T) -> None: ...

    # предусловие: очередь не пустая
    # постусловие: элемент удален из головы очереди
    @abstractmethod
    def remove_front(self) -> None: ...

    # Запросы:
    @abstractmethod
    def size(self) -> int: ...  # размер очереди

    # предусловие: список не пустой
    @abstractmethod
    def get_front(self) -> T: ...  # элемент из головы очереди

    # Дополнительные запросы:
    @abstractmethod
    def get_remove_front_status(self) -> int: ...  # успешно; пустая очередь
    @abstractmethod
    def get_get_front_status(self) -> int: ...  # успешно; пустая очередь


# АТД Queue
class AbsQueue(ParentQueue):

    # Конструктор
    # постусловие: создана пустая очередь
    def __init__(self) -> None: ...


# АТД Deque
class AbsDeque(ParentQueue):

    # Конструктор
    # постусловие: создана пустая очередь
    def __init__(self) -> None: ...

    # Команды:
    # постусловие: новый элемент добавлен в начало очереди
    @abstractmethod
    def add_front(self, value: T) -> None: ...

    # предусловие: очередь не пустая
    # постусловие: элемент удален из хвоста очереди
    @abstractmethod
    def remove_tail(self) -> None: ...

    # Запросы:
    # предусловие: очередь не пустая
    @abstractmethod
    def get_tail(self) -> T: ...  # элемент из хвоста очереди

    # Дополнительные запросы:
    # запросы статусов (возможные значения статусов)
    @abstractmethod
    def get_remove_tail_status(self) -> int: ...  # успешно; пустая очередь
    @abstractmethod
    def get_get_tail_status(self) -> int: ...  # успешно; пустая очередь


# Реализация Deque
class Deque(AbsDeque):

    REMOVE_FRONT_NIL = 0  # remove_front() не вызывалась
    REMOVE_FRONT_OK = 1  # успешно удален элемент из головы очереди
    REMOVE_FRONT_ERR = 2  # очередь пустая

    REMOVE_TAIL_NIL = 0  # remove_tail() не вызывалась
    REMOVE_TAIL_OK = 1  # успешно удален элемент из хвоста очереди
    REMOVE_TAIL_ERR = 2  # очередь пустая

    GET_FRONT_NIL = 0  # get_front() не вызывалась
    GET_FRONT_OK = 1  # успешно получен элемент из головы очереди
    GET_FRONT_ERR = 2  # очередь пустая

    GET_TAIL_NIL = 0  # get_tail() не вызывалась
    GET_TAIL_OK = 1  # успешно получен элемент из хвоста очереди
    GET_TAIL_ERR = 2  # очередь пустая

    def __init__(self) -> None:
        super().__init__()
        self.deque = []
        self._remove_front_status = self.REMOVE_FRONT_NIL
        self._remove_tail_status = self.REMOVE_TAIL_NIL
        self._get_front_status = self.GET_FRONT_NIL
        self._get_tail_status = self.GET_TAIL_NIL

    def add_tail(self, value: T) -> None:
        self.deque.append(value)

    def add_front(self, value: T) -> None:
        self.deque.insert(0, value)

    def remove_front(self) -> None:
        if not self.deque:
            self._remove_front_status = self.REMOVE_FRONT_ERR
            return
        self._remove_front_status = self.REMOVE_FRONT_OK
        self.deque.pop(0)

    def remove_tail(self) -> None:
        if not self.deque:
            self._remove_tail_status = self.REMOVE_TAIL_ERR
            return
        self._remove_tail_status = self.REMOVE_TAIL_OK
        self.deque.pop()

    def get_front(self) -> T:
        if not self.deque:
            self._get_front_status = self.GET_FRONT_ERR
            return
        self._get_front_status = self.GET_FRONT_OK
        return self.deque[0]

    def get_tail(self) -> T:
        if not self.deque:
            self._get_tail_status = self.GET_TAIL_ERR
            return
        self._get_tail_status = self.GET_TAIL_OK
        return self.deque[-1]

    def size(self) -> int:
        return len(self.deque)

    def get_remove_front_status(self) -> int:
        return self._remove_front_status

    def get_remove_tail_status(self) -> int:
        return self._remove_tail_status

    def get_get_tail_status(self) -> int:
        return self._get_tail_status

    def get_get_front_status(self) -> int:
        return self._get_front_status
