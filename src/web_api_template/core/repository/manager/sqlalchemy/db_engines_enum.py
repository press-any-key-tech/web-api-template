import enum


class DbEnginesEnum(enum.Enum):
    """SQL Alchemy db engines

    Args:
        enum (_type_): _description_
    """

    POSTGRES = "POSTGRES"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"

    def __str__(self):
        return self.value
