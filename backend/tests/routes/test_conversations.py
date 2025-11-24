"""Tests for the Conversations endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from app.models.conversation import Conversation
from app.models.pagination import PaginatedResponse
from fastapi.testclient import TestClient


class TestConversationsEndpoints:
    """Test cases for Conversations endpoints."""

    def test_conversations_chats_requires_auth(self, fresh_client: TestClient) -> None:
        """Test that chats endpoint requires authentication."""
        response = fresh_client.get("/api/v1/conversations/chats")
        assert response.status_code == 401

    @patch("app.routes.conversations.settings.CONVERSATION_URL", None)
    def test_conversations_chats_service_disabled(self, authenticated_client: TestClient) -> None:
        """Test that chats endpoint returns 503 when conversation service is disabled."""
        response = authenticated_client.get("/api/v1/conversations/chats")
        assert response.status_code == 503
        data = response.json()
        assert "Conversation service is not configured" in data["msg"]

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_conversations_chats_success(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test successful chats retrieval."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock conversation data
        test_conversations = PaginatedResponse(
            count=2,
            results=[
                Conversation(
                    id="conv-123",
                    title="Project Discussion",
                    created_at="2024-11-01T10:00:00Z",
                    updated_at="2024-11-01T11:00:00Z",
                ),
                Conversation(
                    id="conv-456",
                    title="Team Standup",
                    created_at="2024-11-02T09:00:00Z",
                    updated_at="2024-11-02T10:00:00Z",
                ),
            ],
        )

        # Mock the client instance and its methods
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.return_value = test_conversations
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["results"]) == 2
        assert data["results"][0]["id"] == "conv-123"
        assert data["results"][0]["title"] == "Project Discussion"
        assert data["results"][1]["id"] == "conv-456"
        assert data["results"][1]["title"] == "Team Standup"

        # Verify token exchange was called
        mock_get_token.assert_called_once()

        # Verify ConversationClient was instantiated
        mock_conversation_client.assert_called_once()

        # Verify get_chats was called with default pagination
        mock_client_instance.get_chats.assert_called_once_with(page=1, page_size=5, title=None)

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_docs_get_conversations_chats_with_title_filter(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test conversations retrieval with title filter."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock DocsClient
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.return_value = PaginatedResponse(
            count=1,
            results=[
                Conversation(
                    id="conv-456",
                    title="Filtered Document",
                    created_at="2024-11-01T11:00:00Z",
                    updated_at="2024-11-01T11:00:00Z",
                )
            ],
        )
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats?title=Filtered%20Document")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Filtered Document"

        # Verify DocsClient was called with title filter
        mock_client_instance.get_chats.assert_called_once_with(
            page=1,
            page_size=5,
            title="Filtered Document",
        )

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_conversations_chats_with_pagination(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test chats retrieval with pagination parameter."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock conversation data for page 2
        test_conversations = PaginatedResponse(
            count=1,
            results=[
                Conversation(
                    id="conv-789",
                    title="Client Meeting",
                    created_at="2024-10-30T14:00:00Z",
                    updated_at="2024-10-30T15:00:00Z",
                ),
            ],
        )

        # Mock the client instance and its methods
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.return_value = test_conversations
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats?page=2&page_size=1")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "conv-789"
        assert data["results"][0]["title"] == "Client Meeting"

        # Verify get_chats was called with page=2
        mock_client_instance.get_chats.assert_called_once_with(page=2, page_size=1, title=None)

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_conversations_chats_empty_result(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test chats endpoint with no conversations."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock empty conversation data
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.return_value = PaginatedResponse[Conversation](count=0, results=[])
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    def test_conversations_chats_token_exchange_error(
        self,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test chats endpoint when token exchange fails."""
        from app.exceptions import TokenExchangeError

        # Mock token exchange error
        mock_get_token.side_effect = TokenExchangeError("Token exchange failed")

        response = authenticated_client.get("/api/v1/conversations/chats")

        assert response.status_code == 403  # TokenExchangeError returns 403

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_conversations_chats_client_error(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test chats endpoint when ConversationClient raises an exception."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock ConversationClient error
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.side_effect = httpx.HTTPError("Conversation service error")
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats")

        assert response.status_code == 502  # HTTPError returns 502 Bad Gateway

    @pytest.mark.parametrize(
        "invalid_page",
        [
            "invalid",
            "not-a-number",
        ],
    )
    def test_conversations_chats_invalid_pagination_type(
        self, authenticated_client: TestClient, invalid_page: str
    ) -> None:
        """Test chats endpoint with invalid pagination parameter types."""
        response = authenticated_client.get(f"/api/v1/conversations/chats?page={invalid_page}")
        assert response.status_code == 422  # Unprocessable Entity - type conversion failed

    @patch("app.routes.conversations.settings.CONVERSATION_URL", "https://conversations.example.com")
    @patch("app.routes.conversations.settings.CONVERSATION_AUDIENCE", "conversations")
    @patch("app.routes.conversations.get_token")
    @patch("app.routes.conversations.ConversationClient")
    def test_conversations_chats_with_computed_url_field(
        self,
        mock_conversation_client: MagicMock,
        mock_get_token: MagicMock,
        authenticated_client: TestClient,
    ) -> None:
        """Test that conversations include computed URL field."""
        # Mock token exchange
        mock_get_token.return_value = "test-conversation-token"

        # Mock conversation data
        test_conversations = PaginatedResponse(
            count=1,
            results=[
                Conversation(
                    id="conv-123",
                    title="Project Discussion",
                    created_at="2024-11-01T10:00:00Z",
                    updated_at="2024-11-01T11:00:00Z",
                ),
            ],
        )

        # Mock the client instance and its methods
        mock_client_instance = AsyncMock()
        mock_client_instance.get_chats.return_value = test_conversations
        mock_conversation_client.return_value = mock_client_instance

        response = authenticated_client.get("/api/v1/conversations/chats")

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "conv-123"
        assert data["results"][0]["title"] == "Project Discussion"
        assert data["results"][0]["created_at"] == "2024-11-01T10:00:00Z"
        # Check the computed URL field
        assert "url" in data["results"][0]
        assert data["results"][0]["url"] == "https://conversations.example.com/chat/conv-123/"
