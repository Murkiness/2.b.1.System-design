from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


# АТД NativeDictionary
class AbsNativeDictionary(ABC, Generic[T]):

    # Конструктор
    # постусловие: создан ассоциативный массив
    def __init__(self) -> None: ...

    # Команды:
    # постусловие: если ключа нет в массиве, то новая пара ключ-значение добавлена в массив;
    # если ключ есть в массиве, то обновлено значение ключа
    @abstractmethod
    def put(self, key: str, value: T) -> None: ...

    # предусловие: в массиве есть запрашиваемый ключ
    # постусловие: пара "ключ-значение" удалена из массива
    @abstractmethod
    def remove(self, key: str) -> None: ...

    # Запросы:
    @abstractmethod
    def is_key(self, key: str) -> bool: ...  # есть ключ в массиве или нет
    @abstractmethod
    def size(self) -> int: ...  # кол-во пар "ключ-значение" в массиве
    # предусловие: запрашиваемый ключ есть в массиве
    @abstractmethod
    def get(self, key: str) -> T: ...  # получено значение по ключу

    # Дополнительные запросы:
    # запросы статусов (возможные значения статусов)
    @abstractmethod
    def get_put_status(self) -> int: ...  # добавлена новая пара "ключ-значение";  обновлено значение по ключу

    @abstractmethod
    def get_remove_status(self) -> int: ...  # удалена пара "ключ-значение"; в массиве нет запрашиваемого ключа

    @abstractmethod
    def get_get_status(self) -> int: ...  # получено значение по ключу; в массиве нет запрашиваемого ключа


# Реализация NativeDictionary
class NativeDictionary(AbsNativeDictionary):

    PUT_NIL = 0  # put() не вызывалась
    PUT_OK = 1  # добавлена новая пара "ключ-значение" в массив
    PUT_UPD = 2  # обновлено значение по ключу

    REMOVE_NIL = 0  # remove() не вызывалась
    REMOVE_OK = 1  # удалена пара "ключ-значение" из массива
    REMOVE_ERR = 2  # в массиве нет запрашиваемоего ключа

    GET_NIL = 0  # get() не вызывалась
    GET_OK = 1  #  получено значение по ключу
    GET_ERR = 2  # в массиве нет запрашиваемоего ключа

    def __init__(self) -> None:
        super().__init__()
        self._count = 0
        self._capacity = 16
        self._slots = [None] * self._capacity
        self._values = [None] * self._capacity
        self._put_status = self.PUT_NIL
        self._remove_status = self.REMOVE_NIL
        self._get_status = self.GET_NIL

    def __resize(self, new_capacity):
        new_slots = [None] * new_capacity
        new_values = [None] * new_capacity
        for i in range(self._count):
            new_slots[i] = self._slots[i]
            new_values[i] = self._values[i]
        self._slots = new_slots
        self._values = new_values
        self._capacity = new_capacity

    def _hash_fun(self, key):
        hash = sum([ord(sym) for sym in key]) % self._capacity
        return hash

    def __remove_key_value(self, index: int) -> None:
        for j in range(index, self._capacity - 1):
            self._slots[j] = self._slots[j + 1]
            self._values[j] = self._values[j + 1]
        decrease_capacity = int(self._capacity / 1.5)
        if self._count < self._capacity * 0.5:
            self.__resize(decrease_capacity if decrease_capacity >= 16 else 16)

    def is_key(self, key) -> bool:
        return key in self._slots

    def put(self, key: str, value: T) -> None:
        index = self._hash_fun(key)
        if not self.is_key(key) and self._count == self._capacity:
            self.__resize(2 * self._capacity)
        count = 0
        while count < self._capacity:
            if self.is_key(key) and self._slots[index] == key:
                self._values[index] = value
                self._put_status = self.PUT_UPD
                return
            if not self.is_key(key) and not self._slots[index]:
                self._slots[index] = key
                self._values[index] = value
                self._count += 1
                self._put_status = self.PUT_OK
                return
            index += 1
            if index >= self._capacity:
                index %= self._capacity
            count += 1

    def remove(self, key: str) -> None:
        if not self.is_key(key):
            self._remove_status = self.REMOVE_ERR
            return
        index = self._hash_fun(key)
        count = 0
        while count < self._capacity:
            if self._slots[index] == key:
                self.__remove_key_value(index)
                self._count -= 1
                self._remove_status = self.REMOVE_OK
                return
            index += 1
            if index >= self._capacity:
                index %= self._capacity
            count += 1

    def size(self) -> int:
        return self._count

    def get(self, key: str) -> T:
        if not self.is_key(key):
            self._get_status = self.GET_ERR
            return
        index = self._hash_fun(key)
        count = 0
        while count < self._capacity:
            if self._slots[index] == key:
                self._get_status = self.GET_OK
                return self._values[index]
            index += 1
            if index >= self._capacity:
                index %= self._capacity
            count += 1

    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status

    def get_get_status(self) -> int:
        return self._get_status
