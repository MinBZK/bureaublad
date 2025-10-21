import logging
from collections.abc import AsyncGenerator
from typing import Any

from app.exceptions import ExternalServiceError
from app.models.ai import ChatCompletionRequest, StreamChunk
from openai import APIConnectionError, AuthenticationError, OpenAI

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self, model: str, base_url: str | None, api_key: str | None) -> None:
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.system_prompt = """Je bent een behulpzame assistent voor Nederlandse ambtenaren. Houd je aan de volgende richtlijnen:
      1. Communiceer altijd in formeel, correct Nederlands zonder spreektaal of Engelse leenwoorden.
      2. Gebruik de 'u'-vorm in alle communicatie om respect en professionaliteit te tonen.
      3. Geef duidelijke, beknopte, en feitelijke antwoorden gebaseerd op Nederlandse wet- en regelgeving.
      4. Verwijs waar relevant naar officiële overheidswebsites en -publicaties (.overheid.nl, .rijksoverheid.nl).
      5. Respecteer de AVG en andere privacywetgeving; vraag nooit om persoonlijke gegevens.
      6. Wees neutraal en objectief in politiek gevoelige onderwerpen.
      7. Als je het antwoord niet weet, erken dit direct
      8. Gebruik waar mogelijk de officiële terminologie van de Nederlandse overheid.
      9. Structureer complexe antwoorden met duidelijke kopjes en opsommingstekens voor betere leesbaarheid.
      10. Informeer gebruikers over relevante procedures, termijnen en formulieren bij vragen over overheidsprocessen."""  # noqa: E501

    async def stream_response(self, chat_request: ChatCompletionRequest) -> AsyncGenerator[str, Any]:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": chat_request.prompt},
                ],
                stream=True,
            )

            for chunk in completion:
                response = StreamChunk(
                    id=chunk.id,
                    content=chunk.choices[0].delta.content if chunk.choices else None,
                    finish_reason=chunk.choices[0].finish_reason if chunk.choices else None,
                )
                yield f"{response.model_dump_json()}\n\n"

        except APIConnectionError as e:
            logger.exception("AI provider connection error")
            raise ExternalServiceError("AI", "Connection failed") from e
        except AuthenticationError as e:
            logger.exception("AI provider authentication failed")
            raise ExternalServiceError("AI", "Authentication failed") from e
        except Exception as e:
            logger.exception("AI provider error")
            raise ExternalServiceError("AI", "Service temporarily unavailable") from e
