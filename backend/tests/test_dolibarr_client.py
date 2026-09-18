import httpx
import pytest
import respx

from app.config import Settings
from app.dolibarr.client import DolibarrClient
from app.dolibarr.exceptions import (
    DolibarrAuthError,
    DolibarrClientError,
    DolibarrConnectionError,
    DolibarrNotFoundError,
    DolibarrTimeoutError,
)


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        dolibarr_api_url="https://dolibarr.test/api/index.php",
        dolibarr_api_key="test-key",
        dolibarr_timeout_seconds=1,
    )


@pytest.fixture()
def dolibarr_client(settings: Settings) -> DolibarrClient:
    return DolibarrClient(settings=settings)


@respx.mock
def test_get_success(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        return_value=httpx.Response(200, json=[{"id": "1", "name": "ACME"}])
    )
    result = dolibarr_client.get("/thirdparties")
    assert result == [{"id": "1", "name": "ACME"}]


@respx.mock
def test_get_sends_dolapikey_header_not_query(dolibarr_client: DolibarrClient):
    route = respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        return_value=httpx.Response(200, json=[])
    )
    dolibarr_client.get("/thirdparties")
    sent_request = route.calls[0].request
    assert sent_request.headers["DOLAPIKEY"] == "test-key"
    assert "DOLAPIKEY" not in str(sent_request.url)


@respx.mock
def test_401_raises_auth_error(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        return_value=httpx.Response(401, json={"error": "invalid key"})
    )
    with pytest.raises(DolibarrAuthError):
        dolibarr_client.get("/thirdparties")


@respx.mock
def test_404_raises_not_found(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties/999").mock(
        return_value=httpx.Response(404, json={"error": "not found"})
    )
    with pytest.raises(DolibarrNotFoundError):
        dolibarr_client.get("/thirdparties/999")


@respx.mock
def test_500_raises_client_error(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        return_value=httpx.Response(500, json={"error": "boom"})
    )
    with pytest.raises(DolibarrClientError):
        dolibarr_client.get("/thirdparties")


@respx.mock
def test_timeout_raises_timeout_error(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        side_effect=httpx.TimeoutException("timed out")
    )
    with pytest.raises(DolibarrTimeoutError):
        dolibarr_client.get("/thirdparties")


@respx.mock
def test_connection_error_raises_connection_error(dolibarr_client: DolibarrClient):
    respx.get("https://dolibarr.test/api/index.php/thirdparties").mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    with pytest.raises(DolibarrConnectionError):
        dolibarr_client.get("/thirdparties")


@respx.mock
def test_post_is_not_retried_on_failure(dolibarr_client: DolibarrClient):
    route = respx.post("https://dolibarr.test/api/index.php/thirdparties").mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    with pytest.raises(DolibarrConnectionError):
        dolibarr_client.post("/thirdparties", json={"name": "ACME"})
    assert route.call_count == 1
