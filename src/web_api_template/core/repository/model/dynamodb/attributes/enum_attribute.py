from typing import Any

from pynamodb.attributes import Attribute
from pynamodb.constants import NUMBER, STRING


class EnumAttribute(Attribute[str]):
    """
    A class for enum attributes
    """

    attr_type = STRING

    def __init__(self, *args: Any, enum_type: type, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.enum_type = enum_type

    def serialize(self, value):
        if value is None:
            return None
        else:
            ret_val = str(value.value)
            return ret_val

    def deserialize(self, value):
        return self.enum_type(value)
