from typing import Any


class Mask:
    def __init__(self, mask_value: str = "***MASKED***", mask_keywords: list[str] | None = None) -> None:
        if mask_keywords is None:
            mask_keywords = []
        self.mask_value = mask_value

        # default keywords to mask
        self.keywords: list[str] = ["password", "secret"]
        self.keywords.extend(mask_keywords or [])

    def _should_mask(self, text: str) -> bool:
        """Check if a string contains any sensitive keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)

    def _mask_item(self, item: Any) -> Any:  # noqa: ANN401
        """Mask a string item if it contains sensitive keywords."""
        if isinstance(item, str) and self._should_mask(item):
            return self.mask_value
        return item

    def secrets(self, data: str | list[Any] | dict[Any, Any] | set[Any]) -> str | list[Any] | dict[Any, Any] | set[Any]:
        if isinstance(data, dict):
            masked_dict: dict[Any, Any] = {}
            for key, value in data.items():
                # For dicts: check if KEY contains keyword, mask the VALUE if so
                if isinstance(key, str) and self._should_mask(key):
                    masked_dict[key] = self.mask_value
                else:
                    masked_dict[key] = value
            return masked_dict

        if isinstance(data, list):
            # For lists: check each ITEM and mask the ITEM itself if it contains keyword
            return [self._mask_item(item) for item in data]

        if isinstance(data, set):
            # For sets: check each ITEM and mask the ITEM itself if it contains keyword
            return {self._mask_item(item) for item in data}

        # For strings: mask if contains keyword
        return self._mask_item(data)
