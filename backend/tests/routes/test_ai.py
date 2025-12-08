from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class TestAIChatCompletions:
    """Tests for /ai/chat/completions endpoint."""

    def test_chat_completions_unauthenticated(self, client: TestClient) -> None:
        """Test that chat completions endpoint returns 401 when not authenticated."""
        response = client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})
        assert response.status_code == 401

    @patch("app.core.config.settings.AI_URL", None)
    def test_chat_completions_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test that endpoint returns 503 when AI service is disabled."""
        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})
        assert response.status_code == 503
        data = response.json()
        assert "AI service is not configured" in data["msg"]

    @patch("app.core.config.settings.AI_MODEL", None)
    def test_chat_completions_no_model_configured(self, authenticated_client: TestClient) -> None:
        """Test that endpoint returns 503 when no AI model is configured."""
        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})
        assert response.status_code == 503
        data = response.json()
        assert "AI service is not configured" in data["msg"]

    def test_chat_completions_invalid_request_body(self, authenticated_client: TestClient) -> None:
        """Test that endpoint returns 422 for invalid request body."""
        # Missing required prompt field
        response = authenticated_client.post("/api/v1/ai/chat/completions", json={})
        assert response.status_code == 422

        # Wrong data type for prompt
        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": 123})
        assert response.status_code == 422

    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    @patch("app.clients.ai.AIClient.stream_response")
    def test_chat_completions_success(self, mock_stream_response: MagicMock, authenticated_client: TestClient) -> None:
        """Test successful chat completions request."""

        # Mock the streaming response
        async def mock_stream():
            yield '{"id": "test-1", "content": "Hello", "finish_reason": null}\n\n'
            yield '{"id": "test-2", "content": " there!", "finish_reason": null}\n\n'
            yield '{"id": "test-3", "content": null, "finish_reason": "stop"}\n\n'

        mock_stream_response.return_value = mock_stream()

        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        # Check that AIClient.stream_response was called with the correct request
        mock_stream_response.assert_called_once()
        call_args = mock_stream_response.call_args[1]
        assert call_args["chat_request"].prompt == "Hello, world!"

    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    @patch("app.clients.ai.AIClient.stream_response")
    def test_chat_completions_empty_prompt(
        self, mock_stream_response: MagicMock, authenticated_client: TestClient
    ) -> None:
        """Test chat completions with empty prompt."""

        async def mock_stream():
            yield '{"id": "test-1", "content": "Please provide a prompt.", "finish_reason": "stop"}\n\n'

        mock_stream_response.return_value = mock_stream()

        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": ""})

        assert response.status_code == 200
        mock_stream_response.assert_called_once()

    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    @patch("app.clients.ai.AIClient.stream_response")
    def test_chat_completions_long_prompt(
        self, mock_stream_response: MagicMock, authenticated_client: TestClient
    ) -> None:
        """Test chat completions with a long prompt."""
        long_prompt = "What is the meaning of life? " * 100  # Very long prompt

        async def mock_stream():
            yield '{"id": "test-1", "content": "That is a complex question.", "finish_reason": "stop"}\n\n'

        mock_stream_response.return_value = mock_stream()

        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": long_prompt})

        assert response.status_code == 200
        mock_stream_response.assert_called_once()
        call_args = mock_stream_response.call_args[1]
        assert call_args["chat_request"].prompt == long_prompt

    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    @patch("app.clients.ai.AIClient.stream_response")
    def test_chat_completions_ai_connection_error(
        self, mock_stream_response: MagicMock, authenticated_client: TestClient
    ) -> None:
        """Test chat completions when AI service has connection error."""
        from app.exceptions import ExternalServiceError

        mock_stream_response.side_effect = ExternalServiceError("AI", "Connection failed")

        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})

        assert response.status_code == 502  # Bad Gateway
        data = response.json()
        assert "AI service error" in data["msg"]

    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    @patch("app.clients.ai.AIClient.stream_response")
    def test_chat_completions_ai_auth_error(
        self, mock_stream_response: MagicMock, authenticated_client: TestClient
    ) -> None:
        """Test chat completions when AI service has authentication error."""
        from app.exceptions import ExternalServiceError

        mock_stream_response.side_effect = ExternalServiceError("AI", "Authentication failed")

        response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Hello, world!"})

        assert response.status_code == 502  # Bad Gateway
        data = response.json()
        assert "AI service error" in data["msg"]

    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    def test_chat_completions_special_characters(self, authenticated_client: TestClient) -> None:
        """Test chat completions with special characters in prompt."""
        with patch("app.clients.ai.AIClient.stream_response") as mock_stream_response:

            async def mock_stream():
                yield '{"id": "test-1", "content": "I understand special chars.", "finish_reason": "stop"}\n\n'

            mock_stream_response.return_value = mock_stream()

            special_prompt = "Hello! How are you? 🤖 What about émojis and ñoñó?"

            response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": special_prompt})

            assert response.status_code == 200
            mock_stream_response.assert_called_once()
            call_args = mock_stream_response.call_args[1]
            assert call_args["chat_request"].prompt == special_prompt

    @patch("app.core.config.settings.AI_MODEL", "test-model")
    @patch("app.core.config.settings.AI_URL", "https://api.test.com")
    @patch("app.core.config.settings.AI_API_KEY", "test-key")
    def test_chat_completions_response_format(self, authenticated_client: TestClient) -> None:
        """Test that the response format is correct for streaming."""
        with patch("app.clients.ai.AIClient.stream_response") as mock_stream_response:

            async def mock_stream():
                yield '{"id": "test-1", "content": "Hello", "finish_reason": null}\n\n'
                yield '{"id": "test-2", "content": " world", "finish_reason": null}\n\n'
                yield '{"id": "test-3", "content": "!", "finish_reason": null}\n\n'
                yield '{"id": "test-4", "content": null, "finish_reason": "stop"}\n\n'

            mock_stream_response.return_value = mock_stream()

            response = authenticated_client.post("/api/v1/ai/chat/completions", json={"prompt": "Say hello world"})

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

            # Read the streaming response content
            content = response.content.decode()
            lines = content.strip().split("\n\n")

            # Verify we got the expected number of chunks
            assert len(lines) == 4

            # Each line should be valid JSON
            import json

            for line in lines:
                if line.strip():
                    data = json.loads(line)
                    assert "id" in data
                    assert "content" in data
                    assert "finish_reason" in data
