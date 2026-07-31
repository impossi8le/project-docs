"""Пример пакета для автогенерации документации.

Этот пакет используется как демонстрация того, как mkdocstrings
строит страницы API из docstrings. Замените его на свой реальный код
или удалите вместе со страницей docs/reference/python/example_pkg.md.
"""


class Calculator:
    """Простой калькулятор с поддержкой памяти.

    Пример использования:

    ```python
    calc = Calculator()
    calc.add(2, 3)  # 5
    ```

    Атрибуты:
        memory: Текущее значение в памяти калькулятора.
    """

    def __init__(self) -> None:
        """Создаёт калькулятор с обнулённой памятью."""
        self.memory: float = 0.0

    def add(self, a: float, b: float) -> float:
        """Складывает два числа.

        Args:
            a: Первое слагаемое.
            b: Второе слагаемое.

        Returns:
            Сумма a и b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Вычитает из a число b.

        Args:
            a: Уменьшаемое.
            b: Вычитаемое.

        Returns:
            Разность a и b.
        """
        return a - b

    def store(self, value: float) -> None:
        """Сохраняет значение в память.

        Args:
            value: Число для сохранения в памяти.
        """
        self.memory = value

    def recall(self) -> float:
        """Возвращает значение из памяти.

        Returns:
            Текущее значение memory.
        """
        return self.memory
