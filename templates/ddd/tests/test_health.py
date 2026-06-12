from fastapi.testclient import TestClient

from app.shared.exceptions.domains.chat import ChatError
from app.shared.exceptions.domains.chat.error_code import ChatErrorCode
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
    }
