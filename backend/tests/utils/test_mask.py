"""Tests for the mask utility module."""

import pytest
from app.utils.mask import Mask


class TestMask:
    """Test cases for the Mask class."""

    def test_init_default_values(self) -> None:
        """Test Mask initialization with default values."""
        mask = Mask()
        assert mask.mask_value == "***MASKED***"
        assert "password" in mask.keywords
        assert "secret" in mask.keywords
        assert len(mask.keywords) == 2

    def test_init_custom_mask_value(self) -> None:
        """Test Mask initialization with custom mask value."""
        custom_mask = "[REDACTED]"
        mask = Mask(mask_value=custom_mask)
        assert mask.mask_value == custom_mask
        assert "password" in mask.keywords
        assert "secret" in mask.keywords

    def test_init_custom_keywords(self) -> None:
        """Test Mask initialization with custom keywords."""
        custom_keywords = ["token", "api_key"]
        mask = Mask(mask_keywords=custom_keywords)
        assert mask.mask_value == "***MASKED***"
        assert "password" in mask.keywords
        assert "secret" in mask.keywords
        assert "token" in mask.keywords
        assert "api_key" in mask.keywords
        assert len(mask.keywords) == 4

    def test_init_custom_values_and_keywords(self) -> None:
        """Test Mask initialization with both custom mask value and keywords."""
        custom_mask = "[HIDDEN]"
        custom_keywords = ["auth", "credentials"]
        mask = Mask(mask_value=custom_mask, mask_keywords=custom_keywords)
        assert mask.mask_value == custom_mask
        assert "password" in mask.keywords
        assert "secret" in mask.keywords
        assert "auth" in mask.keywords
        assert "credentials" in mask.keywords

    def test_init_none_keywords(self) -> None:
        """Test Mask initialization with None keywords (should use empty list)."""
        mask = Mask(mask_keywords=None)
        assert len(mask.keywords) == 2
        assert "password" in mask.keywords
        assert "secret" in mask.keywords

    def test_should_mask_case_insensitive(self) -> None:
        """Test that keyword matching is case insensitive."""
        mask = Mask()
        assert mask._should_mask("PASSWORD")
        assert mask._should_mask("Password")
        assert mask._should_mask("password")
        assert mask._should_mask("SECRET")
        assert mask._should_mask("Secret")
        assert mask._should_mask("secret")

    def test_should_mask_substring_matching(self) -> None:
        """Test that keywords are matched as substrings."""
        mask = Mask()
        assert mask._should_mask("user_password")
        assert mask._should_mask("my_secret_key")
        assert mask._should_mask("passwordfield")
        assert mask._should_mask("secretvalue")

    def test_should_mask_false_for_safe_strings(self) -> None:
        """Test that safe strings are not marked for masking."""
        mask = Mask()
        assert not mask._should_mask("username")
        assert not mask._should_mask("email")
        assert not mask._should_mask("normal_text")
        assert not mask._should_mask("safe_value")

    def test_mask_item_string_with_keyword(self) -> None:
        """Test masking a string item that contains keywords."""
        mask = Mask()
        assert mask._mask_item("password123") == "***MASKED***"
        assert mask._mask_item("my_secret") == "***MASKED***"

    def test_mask_item_string_without_keyword(self) -> None:
        """Test that safe string items are not masked."""
        mask = Mask()
        assert mask._mask_item("username") == "username"
        assert mask._mask_item("safe_value") == "safe_value"

    def test_mask_item_non_string(self) -> None:
        """Test that non-string items are never masked."""
        mask = Mask()
        assert mask._mask_item(123) == 123
        assert mask._mask_item(True) is True
        assert mask._mask_item(None) is None
        assert mask._mask_item([1, 2, 3]) == [1, 2, 3]

    def test_secrets_string_masking(self) -> None:
        """Test masking string data."""
        mask = Mask()
        assert mask.secrets("password123") == "***MASKED***"
        assert mask.secrets("my_secret_key") == "***MASKED***"
        assert mask.secrets("username") == "username"
        assert mask.secrets("safe_data") == "safe_data"

    def test_secrets_dict_key_masking(self) -> None:
        """Test masking dictionary data based on keys."""
        mask = Mask()
        data = {"password": "secret123", "username": "john_doe", "api_secret": "abc123", "email": "test@example.com"}
        result = mask.secrets(data)

        assert result["password"] == "***MASKED***"
        assert result["username"] == "john_doe"
        assert result["api_secret"] == "***MASKED***"
        assert result["email"] == "test@example.com"

    def test_secrets_dict_case_insensitive_keys(self) -> None:
        """Test masking dictionary with case insensitive key matching."""
        mask = Mask()
        data = {"PASSWORD": "secret123", "Secret_Key": "abc123", "Username": "john_doe"}
        result = mask.secrets(data)

        assert result["PASSWORD"] == "***MASKED***"
        assert result["Secret_Key"] == "***MASKED***"
        assert result["Username"] == "john_doe"

    def test_secrets_dict_non_string_keys(self) -> None:
        """Test masking dictionary with non-string keys."""
        mask = Mask()
        data = {
            2: "value2",  # Changed from 1 to avoid hash collision with True
            "some_key": "value1",
            None: "value3",
            "password": "secret123",
        }
        result = mask.secrets(data)

        assert result[2] == "value2"
        assert result["some_key"] == "value1"
        assert result[None] == "value3"
        assert result["password"] == "***MASKED***"

    def test_secrets_list_masking(self) -> None:
        """Test masking list data."""
        mask = Mask()
        data = ["username", "password123", "email@test.com", "secret_key"]
        result = mask.secrets(data)

        assert result[0] == "username"
        assert result[1] == "***MASKED***"
        assert result[2] == "email@test.com"
        assert result[3] == "***MASKED***"

    def test_secrets_list_mixed_types(self) -> None:
        """Test masking list with mixed data types."""
        mask = Mask()
        data = ["username", 123, "password123", True, None, "secret_data"]
        result = mask.secrets(data)

        assert result[0] == "username"
        assert result[1] == 123
        assert result[2] == "***MASKED***"
        assert result[3] is True
        assert result[4] is None
        assert result[5] == "***MASKED***"

    def test_secrets_set_masking(self) -> None:
        """Test masking set data."""
        mask = Mask()
        data = {"username", "password123", "email@test.com", "api_secret"}
        result = mask.secrets(data)

        assert "username" in result
        assert "***MASKED***" in result
        assert "email@test.com" in result
        # Check that result has the correct size (sensitive items collapse to one masked value)
        assert len(result) == 3  # username, email, and one ***MASKED*** (both sensitive items become same value)
        # Check that both sensitive strings would be masked
        assert mask._should_mask("password123")
        assert mask._should_mask("api_secret")

    def test_secrets_set_mixed_types(self) -> None:
        """Test masking set with mixed data types."""
        mask = Mask()
        data = {"username", 123, "password123", "safe_value"}
        result = mask.secrets(data)

        assert "username" in result
        assert 123 in result
        assert "***MASKED***" in result
        assert "safe_value" in result
        # Should have exactly one masked item
        masked_count = sum(1 for item in result if item == "***MASKED***")
        assert masked_count == 1

    def test_secrets_empty_collections(self) -> None:
        """Test masking empty collections."""
        mask = Mask()
        assert mask.secrets({}) == {}
        assert mask.secrets([]) == []
        assert mask.secrets(set()) == set()

    def test_custom_mask_value_in_output(self) -> None:
        """Test that custom mask value is used in output."""
        custom_mask = "[REDACTED]"
        mask = Mask(mask_value=custom_mask)

        assert mask.secrets("password123") == custom_mask

        data = {"password": "secret123", "username": "john"}
        result = mask.secrets(data)
        assert result["password"] == custom_mask
        assert result["username"] == "john"

    def test_custom_keywords_masking(self) -> None:
        """Test masking with custom keywords."""
        custom_keywords = ["token", "api_key"]
        mask = Mask(mask_keywords=custom_keywords)

        # Should mask default keywords
        assert mask.secrets("password123") == "***MASKED***"
        assert mask.secrets("secret_data") == "***MASKED***"

        # Should mask custom keywords
        assert mask.secrets("auth_token") == "***MASKED***"
        assert mask.secrets("my_api_key") == "***MASKED***"

        # Should not mask safe strings
        assert mask.secrets("username") == "username"

    def test_edge_cases(self) -> None:
        """Test edge cases and boundary conditions."""
        mask = Mask()

        # Empty string
        assert mask.secrets("") == ""

        # String that is exactly a keyword
        assert mask.secrets("password") == "***MASKED***"
        assert mask.secrets("secret") == "***MASKED***"

        # Very short strings
        assert mask.secrets("a") == "a"
        assert mask.secrets("ab") == "ab"

    def test_immutability_of_input_data(self) -> None:
        """Test that the original input data is not modified."""
        mask = Mask()

        # Test with dictionary
        original_dict = {"password": "secret123", "username": "john"}
        original_dict_copy = original_dict.copy()
        result = mask.secrets(original_dict)
        assert original_dict == original_dict_copy
        assert result != original_dict  # Result should be different

        # Test with list
        original_list = ["username", "password123"]
        original_list_copy = original_list.copy()
        result = mask.secrets(original_list)
        assert original_list == original_list_copy
        assert result != original_list  # Result should be different

    def test_nested_structures_not_recursively_processed(self) -> None:
        """Test that nested structures are not recursively processed."""
        mask = Mask()

        # Nested dict - inner dict should not be processed
        data = {"config": {"password": "secret123"}, "username": "john"}
        result = mask.secrets(data)
        assert result["config"] == {"password": "secret123"}  # Inner dict unchanged
        assert result["username"] == "john"

        # List with nested dict
        data = [{"password": "secret123"}, "username"]
        result = mask.secrets(data)
        assert result[0] == {"password": "secret123"}  # Nested dict unchanged
        assert result[1] == "username"

    @pytest.mark.parametrize(
        ("input_data", "expected"),
        [
            ("password", "***MASKED***"),
            ("secret", "***MASKED***"),
            ("PASSWORD", "***MASKED***"),
            ("SECRET", "***MASKED***"),
            ("username", "username"),
            ("safe_value", "safe_value"),
            ("", ""),
        ],
    )
    def test_string_masking_parametrized(self, input_data: str, expected: str) -> None:
        """Parametrized test for string masking."""
        mask = Mask()
        assert mask.secrets(input_data) == expected

    @pytest.mark.parametrize(
        "mask_value", ["[HIDDEN]", "XXXX", "🔒", "", "a very long mask value with spaces and symbols!@#$%"]
    )
    def test_various_mask_values(self, mask_value: str) -> None:
        """Test various custom mask values."""
        mask = Mask(mask_value=mask_value)
        assert mask.secrets("password123") == mask_value

    @pytest.mark.parametrize(
        "keywords",
        [
            ["token"],
            ["api_key", "auth"],
            ["very_long_keyword_name"],
            [""],  # Empty string keyword
            ["keyword with spaces"],  # Keyword with spaces
        ],
    )
    def test_various_custom_keywords(self, keywords: list[str]) -> None:
        """Test various custom keywords."""
        mask = Mask(mask_keywords=keywords)

        # Default keywords should still work
        assert mask.secrets("password123") == "***MASKED***"

        # Custom keywords should work (if not empty)
        for keyword in keywords:
            if keyword:  # Skip empty keywords
                test_string = f"test_{keyword}_value"
                assert mask.secrets(test_string) == "***MASKED***"
