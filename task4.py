import ctypes
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class AbsDynArray(ABC, Generic[T]):

    # Конструктор
    # постусловие: создан пустой массив
    def __init__(self) -> None: ...

    # Команды:
    # постусловие: новый элемент добавлен в конец массива
    @abstractmethod
    def append(self, value: T) -> None: ...

    # предусловие: i в границах массива;
    # постусловие: новый элемент вставлен в i-позицию
    @abstractmethod
    def insert(self, i: int, value: T) -> None: ...

    # предусловие: i в границах массива;
    # постусловие: элемент i удалён из массива;
    @abstractmethod
    def delete(self, i: int) -> None: ...

    # Запросы:
    # предусловие: i в границах массива;
    @abstractmethod
    def __getitem__(self, i: int) -> T: ...  # значение i-го элемента

    # запросы статусов (возможные значения статусов)
    @abstractmethod
    def get_insert_status(self) -> int: ...  # успешно; индекс за пределами массива
    @abstractmethod
    def get_delete_status(self) -> int: ...  # успешно; индекс за пределами массива
    @abstractmethod
    def get_get_status(self) -> int: ...  # успешно; индекс за пределами массива


# Реализация DynArray
class DynArray(AbsDynArray):

    INSERT_NIL = 0  # insert() еще не вызывалась
    INSERT_OK = 1  # элемент успешно вставлен
    INSERT_ERR = 2  # индекс за пределами массива

    DELETE_NIL = 0  # delete() еще не вызывалась
    DELETE_OK = 1  # элемент успешно удален
    DELETE_ERR = 2  # индекс за пределами массива

    GET_NIL = 0  # get() еще не вызывалась
    GET_OK = 1  # элемент успешно получен
    GET_ERR = 2  # индекс за пределами массива

    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.capacity = 16
        self.array = self.make_array(self.capacity)
        self._insert_status = self.INSERT_NIL
        self._delete_status = self.DELETE_NIL
        self._get_status = self.GET_NIL

    def make_array(self, new_capacity: int):
        return (new_capacity * ctypes.py_object)()

    def _resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, value: T) -> None:
        if self.count == self.capacity:
            self._resize(2 * self.capacity)
        self.array[self.count] = value
        self.count += 1

    def insert(self, i: int, value: T) -> None:
        if i < 0 or i > self.count:
            self._insert_status = self.INSERT_ERR
            return
        if self.count == self.capacity:
            self._resize(2 * self.capacity)
        for j in range(self.count - 1, i - 1, -1):
            self.array[j + 1] = self.array[j]
        self.array[i] = value
        self.count += 1
        self._insert_status = self.INSERT_OK

    def delete(self, i: int) -> None:
        if i < 0 or i >= self.count:
            self._delete_status = self.DELETE_ERR
            return
        for j in range(i, self.count - 1):
            self.array[j] = self.array[j + 1]
        self.count -= 1
        new_capacity = (
            int(self.capacity / 1.5) if int(self.capacity / 1.5) >= 16 else 16
        )
        if self.count < self.capacity * 0.5:
            self._resize(new_capacity)
        self._delete_status = self.DELETE_OK

    def __getitem__(self, i: int) -> T:
        if i < 0 or i >= self.count:
            self._get_status = self.GET_ERR
            return
        self._get_status = self.GET_OK
        return self.array[i]

    def get_insert_status(self) -> int:
        return self._insert_status

    def get_delete_status(self) -> int:
        return self._delete_status

    def get_get_status(self) -> int:
        return self._get_status
