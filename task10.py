from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


# АТД BloomFilter
class AbsBloomFilter(ABC, Generic[T]):

    # Конструктор
    # постусловие: создан фильтр Блюма с битовым массивом размером size
    def __init__(self, size: int) -> None: ...

    # Команды:
    # постусловие: новое значение добавлено в фильтр Блюма
    @abstractmethod
    def add(self, value: T) -> None: ...

    # Запросы:
    # есть ли значение в фильтре Блюма
    def is_value(self, value: T) -> bool: ...


# Реализация BloomFilter
class BloomFilter(AbsBloomFilter):

    def __init__(self, size: int) -> None:
        super().__init__(size)
        self.filter_len = size
        self.filter = 0

    def __hash1(self, str1):
        # 17
        hash = 0
        for c in str1:
            code = ord(c)
            hash = (hash * 17 + code) % self.filter_len
        return 1 << hash

    def __hash2(self, str1):
        # 223
        hash = 0
        for c in str1:
            code = ord(c)
            hash = (hash * 223 + code) % self.filter_len
        return 1 << hash

    def add(self, value: str) -> None:
        self.filter |= (self.__hash1(value) | self.__hash2(value))

    def is_value(self, value: str) -> bool:
        hash1 = self.filter & self.__hash1(value)
        hash2 = self.filter & self.__hash2(value)
        return hash1 > 0 and hash2 > 0
