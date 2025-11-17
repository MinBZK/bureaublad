import gettext
import logging
from contextvars import ContextVar
from pathlib import Path

from fastapi import Request

logger = logging.getLogger(__name__)
_translation_context: ContextVar[gettext.NullTranslations] = ContextVar("translation")


async def set_locale(request: Request) -> None:
    lang = request.headers.get("Accept-Language", "en-US")
    lang = lang.split(",")[0].replace("-", "_")
    logger.debug(f"Setting locale to: {lang}")
    locales_dir = Path(__file__).parent / "../locales"

    translations = gettext.translation("messages", localedir=locales_dir, languages=[lang], fallback=True)
    _translation_context.set(translations)


def _(message: str) -> str:
    try:
        translations = _translation_context.get()
        return translations.gettext(message)
    except LookupError:
        return message
