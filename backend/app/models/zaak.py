from datetime import date

from pydantic import BaseModel

from app.config import settings


class Zaak(BaseModel):
    uuid: str
    url: str
    zaaktype: str
    registratiedatum: date
    startdatum: date
    einddatum: date | None
    omschrijving: str
    status: str | None
