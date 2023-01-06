from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')
PowerSet = TypeVar('PowerSet')


# АТД HashTable
class AbsHashTable(ABC, Generic[T]):

    # Конструктор
    # постусловие: создана пустая хэш-таблица фиксированного размера
    def __init__(self, size: int) -> None: ...

    # Команды:
    # предусловие: в таблице есть свободные слота
    # постусловие: новое значение добавлено в таблицу
    @abstractmethod
    def put(self, value: T) -> None: ...

    # предусловие: в таблице есть запрашиваемое значение
    # постусловие: значение удалено из таблицы
    @abstractmethod
    def remove(self, value: T) -> None: ...

    # Запросы:
    @abstractmethod
    def find(self, value: T) -> bool: ...  # проверка значения в таблице
    @abstractmethod
    def size(self) -> int: ...  # кол-во заполненных слотов в таблице

    # Дополнительные запросы:
    # запросы статусов (возможные значения статусов)
    @abstractmethod
    def get_put_status(self) -> int: ...  # успешно; в таблице нет свободных слотов

    @abstractmethod
    def get_remove_status(self) -> int: ...  # успешно; в таблице нет запрашиваемого значения


# АТД PowerSet
class AbsPowerSet(AbsHashTable):

    # Конструктор
    # постусловие: создано пустое множество фиксированного размера
    def __init__(self, size: int) -> PowerSet: ...

    # Запросы:
    # пересечение текущего множества с множеством set
    @abstractmethod
    def intersection(self, set: PowerSet) -> PowerSet: ...

    # объединение двух множеств
    @abstractmethod
    def union(self, set: PowerSet) -> PowerSet: ...

    # подмножество текущего множества из элементов, которые не входят set
    @abstractmethod
    def difference(self, set: PowerSet) -> PowerSet: ...

    # входят ли все элементы set в текущее множество
    @abstractmethod
    def issubset(self, set: PowerSet) -> bool: ...


# Реализация PowerSet
class PowerSet(AbsPowerSet):

    PUT_NIL = 0  # put() не вызывалась
    PUT_OK = 1  # успешно добавлено новое значение в таблицу
    PUT_ERR = 2  # в таблице нет свободных слотов

    REMOVE_NIL = 0  # remove() не вызывалась
    REMOVE_OK = 1  # успешно значение удалено из таблицы
    REMOVE_ERR = 2  # значения нет в таблице

    def __init__(self, size: int) -> PowerSet:
        super().__init__(size)
        self._size = size
        self.slots = [None] * self._size
        self._count = 0
        self._put_status = self.PUT_NIL
        self._remove_status = self.REMOVE_NIL

    def _hash_fun(self, value: int) -> int:
        if value is None:
            return
        hash = sum([ord(sym) for sym in value]) % self._size
        return hash

    def _seek_slot(self, value: int):
        index = self._hash_fun(value)
        if index is None:
            return
        count = 0
        while count < self._size:
            if not self.slots[index]:
                return index
            index += 1
            if index >= self._size:
                index %= self._size
            count += 1
        return None

    def find(self, value: T) -> bool:
        index = self._hash_fun(value)
        if index is None:
            return
        count = 0
        while count < self._size:
            if self.slots[index] == value:
                return True
            index += 1
            if index >= self._size:
                index %= self._size
            count += 1
        return False

    def put(self, value: T) -> None:
        if self.find(value):
            self._put_status = self.PUT_ERR
            return
        index = self._seek_slot(value)
        if index is None:
            self._put_status = self.PUT_ERR
            return
        self.slots[index] = value
        self._count += 1
        self._put_status = self.PUT_OK

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
            index += 1
            if index >= self._size:
                index %= self._size
            count += 1

    def size(self) -> int:
        return self._count

    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status

    def intersection(self, set: PowerSet) -> PowerSet:
        is_small = self.size() <= set.size()
        small_set, big_set = (self, set) if is_small else (set, self)
        result_set = PowerSet(16)
        for item in small_set.slots:
            if item in big_set.slots:
                if item is None:
                    continue
                result_set.put(item)
        return result_set

    def union(self, set: PowerSet) -> PowerSet:
        is_small = self.size() <= set.size()
        small_set, big_set = (self, set) if is_small else (set, self)
        result = PowerSet(small_set._size + big_set._size)
        for item in big_set.slots:
            if item is None:
                continue
            result.put(item)
        for item in small_set.slots:
            if item is None:
                continue
            result.put(item)
        return result

    def difference(self, set: PowerSet) -> PowerSet:
        for item in set.slots:
            if item is None:
                continue
            self.remove(item)
        return self

    def issubset(self, set: PowerSet) -> bool:
        for item in set.slots:
            if item is None:
                continue
            if item not in self.slots:
                return False
        return True
