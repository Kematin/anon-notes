from enum import Enum


class DatabaseCreateType(str, Enum):
    """
    Тип создаваемой базы данных
    test: Для создания тестовой базы данных
    main: Для создания основной базы данных
    """

    TEST = "test"
    MAIN = "main"
