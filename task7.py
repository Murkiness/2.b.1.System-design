from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


# АТД HashTable
class AbsHashTable(ABC, Generic[T]):

    # Конструктор
    # постусловие: создана пустая хэш-таблица фиксированного размера
    def __init__(self, size: int) -> None: ...

    # Команды:
    # предусловие: в таблице есть свободные слоты
    # постусловие: новое значение добавлено в таблицу
    @abstractmethod
    def put(self, value: T) -> None: ...

    # предусловие: в таблице есть запрашиваемое значение
    # постусловие: значение удалено из таблицы
    @abstractmethod
    def remove(self, value: T) -> None: ...

    # Запросы:
    @abstractmethod
    def find(self, value: T) -> bool: ...  # есть ли значение в таблице
    @abstractmethod
    def size(self) -> int: ...  # кол-во заполненных слотов в таблице

    # Дополнительные запросы:
    # запросы статусов (возможные значения статусов)
    @abstractmethod
    def get_put_status(self) -> int: ...  # успешно; в таблице нет свободных слотов

    @abstractmethod
    def get_remove_status(self) -> int: ...  # успешно; в таблице нет запрашиваемого значения


# Реализация HashTable
class HashTable(AbsHashTable):

    PUT_NIL = 0  # put() не вызывалась
    PUT_OK = 1  # добавлено новое значение в таблицу
    PUT_ERR = 2  # в таблице нет свободных слотов

    REMOVE_NIL = 0  # remove() не вызывалась
    REMOVE_OK = 1  # значение удалено из таблицы
    REMOVE_ERR = 2  # значения нет в таблице

    def __init__(self, size: int) -> None:
        super().__init__(size)
        self._size = size
        self._step = 3
        self._count = 0
        self.slots = [None] * self._size
        self._put_status = self.PUT_NIL
        self._remove_status = self.REMOVE_NIL

    def _hash_fun(self, value: int) -> int:
        hash = sum([ord(sym) for sym in value]) % self._size
        return hash

    def _seek_slot(self, value: int):
        index = self._hash_fun(value)
        count = 0
        while count < self._size:
            if not self.slots[index]:
                return index
            index += self._step
            if index >= self._size:
                index %= self._size
            count += 1
        return None

    def put(self, value: T) -> None:
        index = self._seek_slot(value)
        if not index:
            self._put_status = self.PUT_ERR
            return
        self.slots[index] = value
        self._count += 1
        self._put_status = self.PUT_OK

    def find(self, value: T) -> bool:
        index = self._hash_fun(value)
        count = 0
        while count < self._size:
            if self.slots[index] == value:
                return True
            index += self._step
            if index >= self._size:
                index %= self._size
            count += 1
        return False

    def remove(self, value: T) -> None:
        if not self.find(value):
            self._remove_status = self.REMOVE_ERR
            return
        index = self._hash_fun(value)
        count = 0
        while count < self._size:
            if self.slots[index] == value:
                self.slots[index] = None
                self._count -= 1
                self._remove_status = self.REMOVE_OK
                return
            index += self._step
            if index >= self._size:
                index %= self._size
            count += 1

    def size(self) -> int:
        return self._count

    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status
