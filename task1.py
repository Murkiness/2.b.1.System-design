class BoundedStack:

    # интерфейс класса, реализующий АТД Stack
    POP_NIL = 0  # pop() еще не вызывалась
    POP_OK = 1  # pop() отработала нормально
    POP_ERR = 2  # стек пуст
    PEEK_NIL = 0  # peek() еще не вызывалась
    PEEK_OK = 1  # последняя peek() вернула корректное значение
    PEEK_ERR = 2  # стек пуст
    PUSH_NIL = 0  # push() еще не вызывалась
    PUSH_OK = 1  # элемент добавлен в стек
    PUSH_ERR = 2  # стек переполнен

    # конструктор
    def __init__(self, max_stack_size: int) -> None:
        if (max_stack_size > 0):
            self.max_size = max_stack_size

        self.clear()

    # текущий размер стека
    def size(self) -> int:
        return len(self.stack)

    # добавляет аргумент как новый верхний элемент
    def push(self, value) -> None: #
        if (self.size() < self.max_size):
            self.stack.append(value)
            self.push_status = BoundedStack.PUSH_OK
        else:
            self.push_status = BoundedStack.PUSH_ERR

    # возвращает и удаляет верхний элемент стека
    def pop(self):
        result = None
        if (self.size() > 0):
            result = self.stack.pop()
            self.pop_status = BoundedStack.POP_OK
        else:
            self.pop_status = BoundedStack.POP_ERR

        return result

    # возвращает верхний элемент стека
    def peek(self):
        result = None
        if (self.size() > 0):
            result = self.stack(self.size() - 1)
            self.peek_status = BoundedStack.PEEK_OK
        else:
            self.peek_status = BoundedStack.PEEK_ERR

        return result

    # очищает весь стек
    def clear(self) -> None:
        self.stack = []
        # начальные статусы для предусловий pop(), peek() и push()
        self.pop_status = BoundedStack.POP_NIL
        self.peek_status = BoundedStack.PEEK_NIL
        self.push_status = BoundedStack.PUSH_NIL

    # возвращает максимальное число элементов в стеке
    def get_max_size(self) -> int:
        return self.max_size

    # запросы статусов
    def get_pop_status(self) -> int:
        return self.pop_status

    def get_peek_status(self) -> int:
        return self.peek_status

    def get_push_status(self) -> int:
        return self.push_status
