from abc import ABCMeta, abstractmethod


class HealthcheckRepository(metaclass=ABCMeta):
    """
    Abstract class for database repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def verify(self) -> bool:
        raise NotImplementedError()
