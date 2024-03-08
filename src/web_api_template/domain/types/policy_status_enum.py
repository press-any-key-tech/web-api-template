import enum


class PolicyStatusEnum(enum.Enum):
    """Policy statuses

    Args:
        enum (_type_): _description_
    """

    CREATED = "created"
    VALIDATED = "validated"
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    def __str__(self):
        return self.value
