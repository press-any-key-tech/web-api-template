import enum


class PolicyTypeEnum(enum.Enum):
    """Policy types

    Args:
        enum (_type_): _description_
    """

    HOME = "home"
    LIFE = "life"
    CAR = "car"
    CONTENTS = "contents"

    def __str__(self):
        return self.value
