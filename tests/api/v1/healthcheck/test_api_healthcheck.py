from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import httpx
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from mock import AsyncMock
from pydilite import Provider, configure

from web_api_template.api.v1.healthcheck.api import api_router
from web_api_template.api.v1.healthcheck.response.health_check_response import (
    HealthCheckResponse,
)
from web_api_template.di import include_di

# To patch the method that makes the API call to repository
PATCH_SERVICE: str = "web_api_template.api.v1.healthcheck.api.HealthcheckService"


@pytest.fixture(scope="session")
def app() -> FastAPI:
    # provider: Provider = Provider()
    # include_di(provider=provider)
    # configure(provider=provider)

    app = FastAPI()
    # app.include_router(api_router_healthcheck)
    app.include_router(api_router)

    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def disable_db_initialization():
    with patch("web_api_template.core.settings.settings.INITIALIZE_DATABASE", False):
        yield


@pytest.fixture(autouse=True)
def disable_auth():
    with patch("auth_middleware.settings.settings.AUTH_MIDDLEWARE_DISABLED", True):
        yield


def test_read_main(client):
    response = client.get("/hw")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


@pytest.mark.asyncio
async def test_healthcheck_basic_success(client: TestClient):

    # Act
    response: httpx.Response = client.get("/hc")

    # Assert

    assert response.status_code == 200

    data: Any = response.json()
    assert isinstance(data, dict)

    assert data["status"] == "Healthy"


@pytest.mark.asyncio
async def test_healthcheck_success(client: TestClient):

    expected_result: HealthCheckResponse = HealthCheckResponse(
        status="Healthy", version="1.0.0"
    )

    with patch(PATCH_SERVICE) as service_mock:

        async def async_mock():
            return expected_result

        service_mock.return_value.verify.return_value = async_mock()

        # Act
        response: httpx.Response = client.get("/")  # , params=filter.model_dump())

    # Assert

    assert response.status_code == 200

    data: Any = response.json()
    assert isinstance(data, dict)

    assert data["status"] == "Healthy"


@pytest.mark.asyncio
async def test_healthcheck_error(client: TestClient):

    # Arrange
    # filter: PersonFilter = PersonFilter(name="Person1", surname="Surname1")

    # expected_error: Dict[str, str] = {"detail": "Something went wrong: Simulated error"}

    expected_error: Dict[str, str] = {
        "title": "Internal Server Error",
        "status": 500,
        "detail": "An unexpected error occurred.",
        "instance": "http://testserver/",
    }

    with patch(PATCH_SERVICE) as service_mock:

        service_mock.return_value.verify = AsyncMock(
            side_effect=HTTPException(
                status_code=500, detail="An unexpected error occurred."
            )
        )

        # Act
        response: httpx.Response = client.get("/")  # , params=filter.model_dump())

    # Assert
    assert response.status_code == 500
    assert response.json()["detail"] == expected_error["detail"]
