from typing import List
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest
from ksuid import Ksuid
from sqlalchemy.exc import IntegrityError

from web_api_template.domain.entities import Person, PersonFilter
from web_api_template.infrastructure.models.sqlalchemy import PersonModel
from web_api_template.infrastructure.repositories.sqlalchemy import PersonRepositoryImpl

PERSON_ID: str = str(Ksuid())


@patch(
    "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
    new_callable=MagicMock(),
)
@pytest.mark.asyncio
async def test_create_success(mock_database):
    mock_session = AsyncMock()
    mock_database.return_value.__aenter__.return_value = mock_session

    entity = Person(
        id=PERSON_ID, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    repo = PersonRepositoryImpl()
    result = await repo.create(entity=entity)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert isinstance(result, Person)


# @patch(
#     "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
#     new_callable=MagicMock(),
# )
# @pytest.mark.asyncio
# async def test_create_duplicate_slug(mock_database):
#     mock_session = AsyncMock()
#     mock_database.return_value.__aenter__.return_value = mock_session

#     ksuid: str = str(Ksuid())
#     entity = Person(id=ksuid, name="Test Person", slug="test-person", person_type=1)

#     mock_session.commit.side_effect = IntegrityError(
#         statement="INSERT INTO person (id, name, slug, person_type) VALUES (:id, :name, :slug, :person_type)",
#         params={"id": ksuid, "name": "Test Person", "slug": "test-person", "person_type": 1},
#         orig=Exception("Duplicate key value violates unique constraint"),
#     )

#     repo = PersonRepositoryImpl()

#     with pytest.raises(DuplicatedSlugException):
#         await repo.create(entity=entity)

#     mock_session.add.assert_called_once()
#     mock_session.commit.assert_awaited_once()
#     mock_session.rollback.assert_awaited_once()


# @patch(
#     "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
#     new_callable=MagicMock(),
# )
# @pytest.mark.asyncio
# async def test_create_error(mock_database):
#     mock_session = AsyncMock()
#     mock_database.return_value.__aenter__.return_value = mock_session

#     ksuid: str = str(Ksuid())
#     entity = Person(id=ksuid, name="Test Person", slug="test-person", person_type=1)

#     mock_session.commit.side_effect = Exception("Simulated commit error")

#     repo = PersonRepositoryImpl()

#     with pytest.raises(Exception):
#         await repo.create(entity=entity)

#     mock_session.add.assert_called_once()
#     mock_session.commit.assert_awaited_once()


# # @pytest.fixture
# # def mock_session():
# #     # Crear un mock para la sesión de la base de datos
# #     session = AsyncMock()
# #     session.execute = AsyncMock()
# #     return session


# # @pytest.fixture
# # def mock_db_session(mock_session):
# #     # Mock para Database.get_db_session
# #     with patch(
# #         "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
# #         return_value=mock_session,
# #     ) as mock:
# #         yield mock


# # # @patch(
# # #     "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
# # #     new_callable=MagicMock(),
# # # )
# # @pytest.mark.asyncio
# # async def test_get_list_success(mock_db_session, mock_session):
# #     test_data: List[PersonModel] = [
# #         PersonModel(
# #             id=str(Ksuid()), name="Person 1", slug="person-1", person_type=PersonTypesEnum.coffeeperson
# #         ),
# #         PersonModel(
# #             id=str(Ksuid()), name="Person 2", slug="person-2", person_type=PersonTypesEnum.coffeeperson
# #         ),
# #     ]

# #     mock_db_session.execute.return_value.scalars.return_value.__aenter__.return_value = (
# #         test_data
# #     )

# #     method_filter = PersonFilter(owner_id=1)
# #     repo = PersonRepositoryImpl()
# #     result = await repo.get_list(filter=method_filter)

# #     # mock_database.execute.assert_awaited_once()

# #     assert isinstance(result, list)
# #     assert all(isinstance(item, Person) for item in result)


# # @patch(
# #     "web_api_template.core.repository.manager.sqlalchemy.database.Database.get_db_session",
# #     new_callable=MagicMock(),
# # )
# # @pytest.mark.asyncio
# # async def test_get_list_error(mock_database):
# #     mock_session = AsyncMock()
# #     mock_database.return_value.__aenter__.return_value = mock_session

# #     filter = PersonFilter(owner_id=1)
# #     repo = PersonRepositoryImpl()

# #     mock_session.execute.side_effect = Exception("Simulated database error")

# #     with pytest.raises(Exception):
# #         await repo.get_list(filter=filter)

# #     mock_session.execute.assert_awaited_once_with(select(PersonModel))
