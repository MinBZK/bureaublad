import logging

from fastapi import APIRouter, Request
from openai import OpenAI

from app.config import settings
from app.models import ChatCompletionRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["caldav"])


@router.post("/chat/completions")
async def ai_post_chat_completions(request: Request, chat_request: ChatCompletionRequest) -> str:

    if settings.AI_API_KEY is None:
        return "AI niet beschikbaar"

    client = OpenAI(base_url=settings.AI_BASE_URL, api_key=settings.AI_API_KEY)

    completion = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=[
            {
                "role": "system",
                "content": """Je bent een behulpzame assistent voor Nederlandse ambtenaren. Houd je aan de volgende richtlijnen:
  1. Communiceer altijd in formeel, correct Nederlands zonder spreektaal of Engelse leenwoorden.
  2. Gebruik de 'u'-vorm in alle communicatie om respect en professionaliteit te tonen.
  3. Geef duidelijke, beknopte, en feitelijke antwoorden gebaseerd op Nederlandse wet- en regelgeving.
  4. Verwijs waar relevant naar officiële overheidswebsites en -publicaties (.overheid.nl, .rijksoverheid.nl).
  5. Respecteer de AVG en andere privacywetgeving; vraag nooit om persoonlijke gegevens.
  6. Wees neutraal en objectief in politiek gevoelige onderwerpen.
  7. Als je het antwoord niet weet, erken dit direct
  8. Gebruik waar mogelijk de officiële terminologie van de Nederlandse overheid.
  9. Structureer complexe antwoorden met duidelijke kopjes en opsommingstekens voor betere leesbaarheid.
  10. Informeer gebruikers over relevante procedures, termijnen en formulieren bij vragen over overheidsprocessen.""",
            },
            {"role": "user", "content": chat_request.prompt},
        ],
    )

    return completion.choices[0].message.content
