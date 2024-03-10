from datetime import datetime
from typing import List

import pytest
from ksuid import Ksuid
from mock import AsyncMock, patch
from pydantic import ValidationError

from web_api_template.api.v1.persons.services import ReadService, WriteService
from web_api_template.core.auth.cognito.user import User
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.domain.exceptions import PersonNotFoundException
from web_api_template.infrastructure.models.sqlalchemy import PersonModel

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


def create_person_model() -> PersonModel:

    entity: PersonModel = PersonModel(
        id=PERSON_ID, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    return entity


def create_person_entity() -> Person:

    entity: Person = Person(
        id=PERSON_ID, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    return entity


@pytest.fixture
def mock_repository_create_person() -> AsyncMock:
    model: Person = create_person_model()

    mock_repo = AsyncMock()

    mock_repo.create = AsyncMock(return_value=model)
    return mock_repo


@pytest.fixture
def mock_repository_update_person() -> AsyncMock:
    model: Person = create_person_model()

    mock_repo = AsyncMock()

    mock_repo.update = AsyncMock(return_value=model)
    return mock_repo


@pytest.fixture
def mock_repository_delete() -> AsyncMock:

    entity: Person = create_person_entity()

    mock_repo = AsyncMock()
    mock_repo.get_by_id = AsyncMock(return_value=entity)
    return mock_repo


@pytest.fixture
def mock_repository_not_found_exception() -> AsyncMock:
    mock_repo = AsyncMock()
    mock_repo.delete = AsyncMock(side_effect=ItemNotFoundException)
    return mock_repo


@pytest.fixture
def mock_repository_update_not_found_exception() -> AsyncMock:
    mock_repo = AsyncMock()
    mock_repo.update = AsyncMock(side_effect=ItemNotFoundException)
    return mock_repo


@pytest.mark.asyncio
async def test_create_person(mock_repository_create_person):

    service: WriteService = WriteService(
        person_db_repo=mock_repository_create_person,
    )

    # current_user: User = create_user_entity()

    request: Person = create_person_entity()

    result: Person = await service.create(request=request)

    assert result.id == request.id
    assert result.name == request.name

    # TODO: check parameters
    mock_repository_create_person.create.assert_called_once()

    # Assert surname
    assert result.surname == "Surname1"


@pytest.mark.asyncio
async def test_delete_person(mock_repository_delete):

    # current_user: User = create_user_entity()

    service: WriteService = WriteService(
        person_db_repo=mock_repository_delete,
    )

    await service.delete_by_id(id=PERSON_ID)

    mock_repository_delete.delete.assert_called_once()
    mock_repository_delete.delete.assert_called_once_with(id=PERSON_ID)


@pytest.mark.asyncio
async def test_delete_person_not_found_exception(mock_repository_not_found_exception):

    # current_user: User = create_user_entity()

    service: WriteService = WriteService(
        person_db_repo=mock_repository_not_found_exception,
    )

    with pytest.raises(PersonNotFoundException):
        await service.delete_by_id(id=PERSON_ID)


@pytest.mark.asyncio
async def test_update_person(mock_repository_update_person):

    service: WriteService = WriteService(
        person_db_repo=mock_repository_update_person,
    )

    # current_user: User = create_user_entity()

    request: Person = create_person_entity()

    result: Person = await service.update(id=PERSON_ID, request=request)

    assert result.id == request.id
    assert result.name == request.name

    # TODO: check parameters
    mock_repository_update_person.update.assert_called_once()

    # Assert slug
    assert result.surname == "Surname1"


@pytest.mark.asyncio
async def test_update_person_not_found_exception(
    mock_repository_update_not_found_exception,
):

    # current_user: User = create_user_entity()

    request: Person = create_person_entity()

    service: WriteService = WriteService(
        person_db_repo=mock_repository_update_not_found_exception,
    )

    with pytest.raises(PersonNotFoundException):
        await service.update(id=PERSON_ID, request=request)
