"""Tests for the AI client."""

from unittest.mock import MagicMock, patch

import pytest
from app.clients.ai import AIClient
from app.exceptions import ExternalServiceError
from app.models.ai import ChatCompletionRequest
from openai import AuthenticationError


class MockOpenAIChunk:
    """Mock class for OpenAI completion chunks."""

    def __init__(self, chunk_id: str, content: str | None = None, finish_reason: str | None = None) -> None:
        self.id = chunk_id
        self.choices = [MagicMock()]
        if content is not None:
            self.choices[0].delta.content = content
        else:
            self.choices[0].delta.content = None
        self.choices[0].finish_reason = finish_reason


class TestAIClient:
    """Test cases for the AIClient class."""

    @pytest.fixture
    def ai_client(self) -> AIClient:
        """Create an AIClient instance for testing."""
        return AIClient(model="gpt-3.5-turbo", base_url="https://api.openai.com/v1", api_key="test-api-key")

    def test_init(self) -> None:
        """Test AIClient initialization."""
        with patch("app.clients.ai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client

            client = AIClient(model="gpt-4", base_url="https://api.example.com/v1", api_key="test-key")

            # Verify OpenAI client was created with correct parameters
            mock_openai.assert_called_once_with(base_url="https://api.example.com/v1", api_key="test-key")

            assert client.client == mock_client
            assert client.model == "gpt-4"
            assert "Nederlandse ambtenaren" in client.system_prompt
            assert "officiële terminologie" in client.system_prompt

    def test_init_with_none_values(self) -> None:
        """Test AIClient initialization with None values."""
        with patch("app.clients.ai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client

            client = AIClient(model="gpt-3.5-turbo", base_url=None, api_key=None)

            mock_openai.assert_called_once_with(base_url=None, api_key=None)

            assert client.model == "gpt-3.5-turbo"

    @pytest.mark.asyncio
    async def test_stream_response_success(self, ai_client: AIClient) -> None:
        """Test successful streaming response."""
        # Mock completion chunks
        mock_chunks = [
            MockOpenAIChunk("chunk-1", "Hello"),
            MockOpenAIChunk("chunk-2", " world"),
            MockOpenAIChunk("chunk-3", "!", finish_reason="stop"),
        ]

        # Mock OpenAI completion
        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        # Test the streaming
        chat_request = ChatCompletionRequest(prompt="Test prompt")
        responses = []

        async for response in ai_client.stream_response(chat_request):
            responses.append(response)

        # Verify the OpenAI API call
        ai_client.client.chat.completions.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ai_client.system_prompt},
                {"role": "user", "content": "Test prompt"},
            ],
            stream=True,
        )

        # Verify responses
        assert len(responses) == 3

        # Check first response
        assert "chunk-1" in responses[0]
        assert "Hello" in responses[0]
        assert responses[0].endswith("\n\n")

        # Check second response
        assert "chunk-2" in responses[1]
        assert " world" in responses[1]

        # Check third response (with finish_reason)
        assert "chunk-3" in responses[2]
        assert "!" in responses[2]
        assert "stop" in responses[2]

    @pytest.mark.asyncio
    async def test_stream_response_with_empty_chunks(self, ai_client: AIClient) -> None:
        """Test streaming response with empty content chunks."""
        # Mock completion chunks with some empty content
        mock_chunks = [
            MockOpenAIChunk("chunk-1", "Hello"),
            MockOpenAIChunk("chunk-2", None),  # Empty content
            MockOpenAIChunk("chunk-3", "world"),
        ]

        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="Test prompt")
        responses = []

        async for response in ai_client.stream_response(chat_request):
            responses.append(response)

        assert len(responses) == 3

        # First chunk has content
        assert "Hello" in responses[0]

        # Second chunk has null content
        assert '"content": null' in responses[1] or '"content":null' in responses[1]

        # Third chunk has content
        assert "world" in responses[2]

    @pytest.mark.asyncio
    async def test_stream_response_with_no_choices(self, ai_client: AIClient) -> None:
        """Test streaming response with chunks that have no choices."""
        # Create a mock chunk with no choices
        mock_chunk = MagicMock()
        mock_chunk.id = "chunk-1"
        mock_chunk.choices = []

        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter([mock_chunk])

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="Test prompt")
        responses = []

        async for response in ai_client.stream_response(chat_request):
            responses.append(response)

        assert len(responses) == 1
        assert "chunk-1" in responses[0]
        assert '"content": null' in responses[0] or '"content":null' in responses[0]

    @pytest.mark.asyncio
    async def test_stream_response_authentication_error(self, ai_client: AIClient) -> None:
        """Test streaming response with authentication error."""
        ai_client.client.chat.completions.create = MagicMock(
            side_effect=AuthenticationError("Invalid API key", response=MagicMock(), body=None)
        )

        chat_request = ChatCompletionRequest(prompt="Test prompt")

        with pytest.raises(ExternalServiceError) as exc_info:
            async for _ in ai_client.stream_response(chat_request):
                pass

        assert "AI service error" in str(exc_info.value.detail)
        assert "Authentication failed" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_stream_response_generic_error(self, ai_client: AIClient) -> None:
        """Test streaming response with generic error."""
        ai_client.client.chat.completions.create = MagicMock(side_effect=ValueError("Something went wrong"))

        chat_request = ChatCompletionRequest(prompt="Test prompt")

        with pytest.raises(ExternalServiceError) as exc_info:
            async for _ in ai_client.stream_response(chat_request):
                pass

        assert "AI service error" in str(exc_info.value.detail)
        assert "Service temporarily unavailable" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_stream_response_multiple_prompts(self, ai_client: AIClient) -> None:
        """Test streaming responses for multiple different prompts."""
        # Mock completion chunks for first request
        mock_chunks_1 = [MockOpenAIChunk("chunk-1", "Response 1")]
        mock_completion_1 = MagicMock()
        mock_completion_1.__iter__ = lambda self: iter(mock_chunks_1)

        # Mock completion chunks for second request
        mock_chunks_2 = [MockOpenAIChunk("chunk-2", "Response 2")]
        mock_completion_2 = MagicMock()
        mock_completion_2.__iter__ = lambda self: iter(mock_chunks_2)

        ai_client.client.chat.completions.create = MagicMock(side_effect=[mock_completion_1, mock_completion_2])

        # First request
        chat_request_1 = ChatCompletionRequest(prompt="First prompt")
        responses_1 = []
        async for response in ai_client.stream_response(chat_request_1):
            responses_1.append(response)

        # Second request
        chat_request_2 = ChatCompletionRequest(prompt="Second prompt")
        responses_2 = []
        async for response in ai_client.stream_response(chat_request_2):
            responses_2.append(response)

        # Verify both calls were made with correct prompts
        assert ai_client.client.chat.completions.create.call_count == 2

        # Check first call
        first_call = ai_client.client.chat.completions.create.call_args_list[0]
        assert first_call[1]["messages"][1]["content"] == "First prompt"

        # Check second call
        second_call = ai_client.client.chat.completions.create.call_args_list[1]
        assert second_call[1]["messages"][1]["content"] == "Second prompt"

        # Verify responses are different
        assert "Response 1" in responses_1[0]
        assert "Response 2" in responses_2[0]

    @pytest.mark.asyncio
    async def test_stream_response_system_prompt_included(self, ai_client: AIClient) -> None:
        """Test that system prompt is always included in requests."""
        mock_chunks = [MockOpenAIChunk("chunk-1", "Test response")]
        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="User question")

        # Consume the generator
        async for _ in ai_client.stream_response(chat_request):
            pass

        # Verify the call included both system and user messages
        call_args = ai_client.client.chat.completions.create.call_args
        messages = call_args[1]["messages"]

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == ai_client.system_prompt
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "User question"

    @pytest.mark.asyncio
    async def test_stream_response_model_parameter(self, ai_client: AIClient) -> None:
        """Test that the correct model is used in API calls."""
        mock_chunks = [MockOpenAIChunk("chunk-1", "Test")]
        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="Test")

        async for _ in ai_client.stream_response(chat_request):
            pass

        # Verify the model parameter
        call_args = ai_client.client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-3.5-turbo"
        assert call_args[1]["stream"] is True

    @pytest.mark.asyncio
    async def test_stream_response_json_formatting(self, ai_client: AIClient) -> None:
        """Test that responses are properly formatted as JSON with newlines."""
        mock_chunks = [MockOpenAIChunk("test-id", "Hello", "stop")]

        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="Test")

        responses = []
        async for response in ai_client.stream_response(chat_request):
            responses.append(response)

        assert len(responses) == 1
        response = responses[0]

        # Should end with double newline
        assert response.endswith("\n\n")

        # Should be valid JSON (can be parsed)
        import json

        json_part = response.rstrip("\n")
        parsed = json.loads(json_part)

        assert parsed["id"] == "test-id"
        assert parsed["content"] == "Hello"
        assert parsed["finish_reason"] == "stop"

    def test_system_prompt_content(self, ai_client: AIClient) -> None:
        """Test that system prompt contains expected Dutch government guidelines."""
        system_prompt = ai_client.system_prompt

        # Check for key Dutch government assistant characteristics
        assert "Nederlandse ambtenaren" in system_prompt
        assert "u'-vorm" in system_prompt
        assert "AVG" in system_prompt  # Privacy regulation
        assert "overheid.nl" in system_prompt
        assert "rijksoverheid.nl" in system_prompt
        assert "officiële terminologie" in system_prompt
        assert "formeel, correct Nederlands" in system_prompt
        assert "neutraal en objectief" in system_prompt

    @pytest.mark.asyncio
    async def test_stream_response_long_conversation(self, ai_client: AIClient) -> None:
        """Test streaming with a longer conversation (multiple chunks)."""
        # Simulate a longer response with many chunks
        mock_chunks = [
            MockOpenAIChunk("chunk-1", "Dit"),
            MockOpenAIChunk("chunk-2", " is"),
            MockOpenAIChunk("chunk-3", " een"),
            MockOpenAIChunk("chunk-4", " lange"),
            MockOpenAIChunk("chunk-5", " reactie"),
            MockOpenAIChunk("chunk-6", " in"),
            MockOpenAIChunk("chunk-7", " het"),
            MockOpenAIChunk("chunk-8", " Nederlands"),
            MockOpenAIChunk("chunk-9", ".", finish_reason="stop"),
        ]

        mock_completion = MagicMock()
        mock_completion.__iter__ = lambda self: iter(mock_chunks)

        ai_client.client.chat.completions.create = MagicMock(return_value=mock_completion)

        chat_request = ChatCompletionRequest(prompt="Geef een lange reactie")

        responses = []
        async for response in ai_client.stream_response(chat_request):
            responses.append(response)

        assert len(responses) == 9

        # Verify all chunks are present and in order
        expected_content = ["Dit", " is", " een", " lange", " reactie", " in", " het", " Nederlands", "."]
        for i, expected in enumerate(expected_content):
            assert expected in responses[i]

        # Last chunk should have finish_reason
        assert "stop" in responses[-1]

    @pytest.mark.parametrize("model_name", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "custom-model"])
    def test_different_models(self, model_name: str) -> None:
        """Test AIClient with different model names."""
        with patch("app.clients.ai.OpenAI") as mock_openai:
            client = AIClient(model=model_name, base_url="https://api.openai.com/v1", api_key="test-key")

            assert client.model == model_name
            mock_openai.assert_called_once()

    @pytest.mark.parametrize(
        ("base_url", "api_key"),
        [
            ("https://api.openai.com/v1", "sk-test123"),
            ("https://custom.ai/v1", "custom-key"),
            (None, None),
            ("", ""),
        ],
    )
    def test_different_configurations(self, base_url: str | None, api_key: str | None) -> None:
        """Test AIClient with different base URLs and API keys."""
        with patch("app.clients.ai.OpenAI") as mock_openai:
            client = AIClient(model="gpt-3.5-turbo", base_url=base_url, api_key=api_key)

            mock_openai.assert_called_once_with(base_url=base_url, api_key=api_key)
            assert client.model == "gpt-3.5-turbo"
