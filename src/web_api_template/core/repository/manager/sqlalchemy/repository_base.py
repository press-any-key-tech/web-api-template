from abc import ABCMeta




class RepositoryBase(metaclass=ABCMeta):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    _label: str

    def __init__(self, label: str = "DEFAULT"):
        """Initialize the repository

        Args:
            label (str, optional): label for the configuration to recover. Defaults to 'DEFAULT'.
        """
        self._label = label
