# from typing import Any, Dict, List
# from unittest.mock import MagicMock, patch

# import httpx
# import pytest
# from fastapi import FastAPI, HTTPException
# from fastapi.testclient import TestClient
# from ksuid import Ksuid
# from mock import AsyncMock
# from pydilite import Provider, configure

# from web_api_template.api.v1.persons.api_persons import api_router
# from web_api_template.core.repository.manager.sqlalchemy.page import Page
# from web_api_template.di import include_di
# from web_api_template.domain.entities.person import Person
# from web_api_template.domain.entities.person_filter import PersonFilter
# from web_api_template.domain.exceptions import PersonNotFoundException

# To patch the method that makes the API call to repository
# PATCH_READ_SERVICE: str = "web_api_template.api.v1.persons.api_persons.ReadService"
# PATCH_WRITE_SERVICE: str = "web_api_template.api.v1.persons.api_persons.WriteService"


# @pytest.fixture(scope="session")
# def app() -> FastAPI:
#     provider: Provider = Provider()
#     include_di(provider=provider)
#     configure(provider=provider)

#     app = FastAPI()
#     app.include_router(api_router_healthcheck)
#     app.include_router(api_router)

#     return app


# @pytest.fixture(scope="session")
# def client(app: FastAPI) -> TestClient:
#     with TestClient(app) as client:
#         yield client


# @pytest.fixture(autouse=True)
# def disable_db_initialization():
#     with patch("web_api_template.core.settings.settings.INITIALIZE_DATABASE", False):
#         yield


# @pytest.fixture(autouse=True)
# def disable_auth():
#     with patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True):
#         yield


# @pytest.fixture
# def mock_repository_exception() -> AsyncMock:
#     mock_repo = AsyncMock()
#     mock_repo.get_list = AsyncMock(side_effect=Exception("Simulated error"))
#     return mock_repo


# @pytest.mark.asyncio
# async def test_get_list_success(client: TestClient):

#     Arrange
#     items: List[Person] = [
#         Person(
#             id=str(Ksuid()),
#             name="Person1",
#             surname="Surname1",
#             email="email1@mail.com",
#             identification_number="1234",
#         ),
#         Person(
#             id=str(Ksuid()),
#             name="Person2",
#             surname="Surname2",
#             email="email2@mail.com",
#             identification_number="5678",
#         ),
#         Person(
#             id=str(Ksuid()),
#             name="Person3",
#             surname="Surname3",
#             email="email3@mail.com",
#             identification_number="4321",
#         ),
#     ]

#     expected_result: Page = Page(
#         items=items,
#         total=3,
#         page=1,
#         size=10,
#     )

#     with patch(PATCH_READ_SERVICE) as service_mock:

#         async def async_mock():
#             return expected_result

#         service_mock.return_value.get_list.return_value = async_mock()

#         Act
#         response: httpx.Response = client.get("/")  # , params=filter.model_dump())

#         service_mock.return_value.get_list.assert_called_once_with(filter=filter)
#         service_mock.return_value.get_list.assert_called_once()

#     Assert

#     assert response.status_code == 200

#     data: Any = response.json()
#     assert isinstance(data, dict)

#     persons: List[Person] = [Person.model_validate(item) for item in data["items"]]
#     assert len(persons) == len(items)
#     assert persons == items


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_get_list_error():

#     # Arrange
#     # filter: PersonFilter = PersonFilter(name="Person1", surname="Surname1")

#     # expected_error: Dict[str, str] = {"detail": "Something went wrong: Simulated error"}

#     expected_error: Dict[str, str] = {
#         "title": "Internal Server Error",
#         "status": 500,
#         "detail": "An unexpected error occurred.",
#         "instance": "http://testserver/",
#     }

#     with patch(PATCH_READ_SERVICE) as service_mock:

#         service_mock.return_value.get_list = AsyncMock(
#             side_effect=HTTPException(
#                 status_code=500, detail="An unexpected error occurred."
#             )
#         )

#         # Act
#         response: httpx.Response = client.get("/")  # , params=filter.model_dump())

#     # Assert
#     assert response.status_code == 500
#     assert response.json()["detail"] == expected_error["detail"]


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_get_by_id_success():
#     # Arrange
#     id: str = str(Ksuid())

#     expected_result = Person(
#         id=id,
#         name="Person1",
#         surname="Surname1",
#         email="email1@mail.com",
#         identification_number="1234",
#     )

#     with patch(PATCH_READ_SERVICE) as service_mock:

#         async def async_mock():
#             return expected_result

#         service_mock.return_value.get_by_id.return_value = async_mock()

#         # Act
#         response: httpx.Response = client.get(f"/{id}")

#         # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
#         service_mock.return_value.get_by_id.assert_called_once()

#     # Assert

#     assert response.status_code == 200

#     data: Any = response.json()

#     person: Person = Person.model_validate(data)
#     assert person == expected_result


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_get_by_id_error_not_found():

#     id: str = str(Ksuid())

#     expected_error: Dict[str, str] = {"detail": f"Person with ID {id} not found"}

#     with patch(PATCH_READ_SERVICE) as service_mock:

#         service_mock.return_value.get_by_id = MagicMock(
#             side_effect=PersonNotFoundException(id=id)
#         )

#         # Act
#         response: httpx.Response = client.get(f"/{id}")

#     # Assert
#     assert response.status_code == 404
#     assert response.json() == expected_error


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_create_success():
#     # Arrange
#     id: str = str(Ksuid())

#     expected_result = Person(
#         id=id,
#         name="Person1",
#         surname="Surname1",
#         email="email1@mail.com",
#         identification_number="1234",
#     )

#     body: Dict[str, str] = {
#         "id": id,
#         "name": "Person1",
#         "surname": "Surname1",
#         "email": "email1@mail.com",
#         "identification_number": "1234",
#     }

#     with patch(PATCH_WRITE_SERVICE) as service_mock:

#         async def async_mock():
#             return expected_result

#         service_mock.return_value.create.return_value = async_mock()

#         # Act
#         response: httpx.Response = client.post("/", json=body)

#         # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
#         service_mock.return_value.create.assert_called_once()

#     # Assert

#     assert response.status_code == 201

#     data: Any = response.json()

#     person: Person = Person.model_validate(data)
#     assert person == expected_result


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_delete_by_id_success():
#     # Arrange
#     id: str = str(Ksuid())

#     with patch(PATCH_WRITE_SERVICE) as service_mock:

#         async def async_mock():
#             return None

#         service_mock.return_value.delete_by_id.return_value = async_mock()

#         # Act
#         response: httpx.Response = client.delete(f"/{id}")

#         # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
#         service_mock.return_value.delete_by_id.assert_called_once()

#     # Assert

#     assert response.status_code == 204


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_delete_by_id_error_not_found():

#     id: str = str(Ksuid())

#     expected_error: Dict[str, str] = {"detail": f"Person with ID {id} not found"}

#     with patch(PATCH_WRITE_SERVICE) as service_mock:

#         service_mock.return_value.delete_by_id = MagicMock(
#             side_effect=PersonNotFoundException(id=id)
#         )

#         # Act
#         response: httpx.Response = client.delete(f"/{id}")

#     # Assert
#     assert response.status_code == 404
#     assert response.json() == expected_error


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_update_success():
#     # Arrange
#     id: str = str(Ksuid())

#     expected_result = Person(
#         id=id,
#         name="Person1",
#         surname="Surname1",
#         email="email1@mail.com",
#         identification_number="1234",
#     )

#     body: Dict[str, str] = {
#         "id": id,
#         "name": "Person1",
#         "surname": "Surname1",
#         "email": "email1@mail.com",
#         "identification_number": "1234",
#     }

#     with patch(PATCH_WRITE_SERVICE) as service_mock:

#         async def async_mock():
#             return expected_result

#         service_mock.return_value.update.return_value = async_mock()

#         # Act
#         response: httpx.Response = client.put(f"/{id}", json=body)

#         # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
#         service_mock.return_value.update.assert_called_once()

#     # Assert

#     assert response.status_code == 200

#     data: Any = response.json()

#     person: Person = Person.model_validate(data)
#     assert person == expected_result


# @patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True)
# @pytest.mark.asyncio
# async def test_update_error_not_found():
#     # Arrange
#     id: str = str(Ksuid())

#     body: Dict[str, str] = {
#         "id": id,
#         "name": "Person1",
#         "surname": "Surname1",
#         "email": "email1@mail.com",
#         "identification_number": "1234",
#     }

#     expected_error: Dict[str, str] = {"detail": f"Person with ID {id} not found"}

#     with patch(PATCH_WRITE_SERVICE) as service_mock:

#         service_mock.return_value.update = MagicMock(
#             side_effect=PersonNotFoundException(id=id)
#         )

#         # Act
#         response: httpx.Response = client.put(f"/{id}", json=body)

#     # Assert
#     assert response.status_code == 404
#     assert response.json() == expected_error
