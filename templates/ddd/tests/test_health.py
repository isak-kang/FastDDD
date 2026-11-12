from fastapi.testclient import TestClient

from app.shared.exceptions.domains.chat import ChatError
from app.shared.exceptions.domains.chat.error_code import ChatErrorCode
from app.shared.response.api_response import ApiResponse
from main import create_app


def test_health_returns_api_response() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "code": "COMMON_SUCCESS",
        "message": "",
        "data": {"status": "ok"},
    }
    # Server-side processing time header (shown in Swagger response headers).
    assert float(response.headers["X-Process-Time-Ms"]) >= 0.0


def test_chat_error_returns_api_error_response() -> None:
    app = create_app()

    @app.get("/raise-chat-error")
    async def raise_chat_error() -> None:
        raise ChatError(ChatErrorCode.CHAT_PROVIDER_FAILED)

    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/raise-chat-error")

    assert response.status_code == 500
    assert response.json() == {
        "status": 500,
        "code": "CHAT_003",
        "message": "Chat provider request failed.",
        "data": None,
    }


def test_unhandled_exception_returns_common_server_error() -> None:
    app = create_app()

    @app.get("/raise-unexpected")
    async def raise_unexpected() -> None:
        raise RuntimeError("boom")

    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/raise-unexpected")

    assert response.status_code == 500
    assert response.json() == {
        "status": 500,
        "code": "COMMON_INTERNAL_SERVER_ERROR",
        "message": "Internal server error.",
        "data": None,
    }


def test_no_content_is_http_200_with_null_data() -> None:
    assert ApiResponse.no_content().to_dict() == {
        "status": 200,
        "code": "COMMON_NO_CONTENT",
        "message": "",
        "data": None,
    }
