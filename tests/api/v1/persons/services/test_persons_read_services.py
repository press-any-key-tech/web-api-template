from typing import List

import pytest
from ksuid import Ksuid
from mock import AsyncMock, patch

from web_api_template.api.v1.persons.services import ReadService
from web_api_template.core.auth.cognito.user import User
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.infrastructure.models.sqlalchemy.person_model import PersonModel

PERSON_ID: str = str(Ksuid())


# TODO: change to utils module
def create_user_entity() -> User:

    user_entity: User = User(
        id="admin_user",
        name="admin",
        email="email@email.com",
        groups=["admin"],
    )

    return user_entity


def create_persons_model() -> List[PersonModel]:
    entity: List[PersonModel] = [
        PersonModel(
            id=str(Ksuid()), name="Person1", surname="Surname1", email="email1@mail.com"
        ),
        PersonModel(
            id=str(Ksuid()), name="Person2", surname="Surname2", email="email2@mail.com"
        ),
        PersonModel(
            id=str(Ksuid()), name="Person3", surname="Surname3", email="email3@mail.com"
        ),
    ]

    return entity


def create_person_entity() -> PersonModel:

    entity: PersonModel = PersonModel(
        id=PERSON_ID, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    return entity


@pytest.fixture
def mock_db_list() -> AsyncMock:

    model_result: List[PersonModel] = create_persons_model()

    mock_repo = AsyncMock()
    mock_repo.get_list = AsyncMock(return_value=model_result)
    return mock_repo


@pytest.fixture
def mock_db_id() -> AsyncMock:
    entity: Person = create_person_entity()

    mock_repo = AsyncMock()
    mock_repo.get_by_id = AsyncMock(return_value=entity)
    return mock_repo


@pytest.fixture
def mock_repository_not_found_exception() -> AsyncMock:
    mock_repo = AsyncMock()
    mock_repo.get_by_id = AsyncMock(side_effect=ItemNotFoundException)
    return mock_repo


@pytest.mark.asyncio
async def test_list_persons(mock_db_list):

    admin_user: User = create_user_entity()

    service: ReadService = ReadService(person_db_repo=mock_db_list)
    person_filter: PersonFilter = PersonFilter()
    result: List[Person] = await service.get_list(filter=person_filter)

    assert len(result) == 3
    assert result[0].name == "Person1"
    assert result[1].surname == "Surname2"
    assert result[2].email == "email3@mail.com"


@pytest.mark.asyncio
async def test_get_person_by_id(mock_db_id):

    service: ReadService = ReadService(person_db_repo=mock_db_id)
    result: Person = await service.get_by_id(id=PERSON_ID)

    assert result.id == PERSON_ID
    assert result.name == "Person1"
    assert result.email == "email1@mail.com"


@pytest.mark.asyncio
async def test_get_person_by_id_person_not_found_exception(
    mock_repository_not_found_exception,
):

    service: ReadService = ReadService(
        person_db_repo=mock_repository_not_found_exception
    )

    with pytest.raises(PersonNotFoundException):
        result: Person = await service.get_by_id(id=PERSON_ID)
