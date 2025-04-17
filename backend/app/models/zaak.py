from datetime import date

from pydantic import BaseModel


class Zaak(BaseModel):
    uuid: str
    url: str
    zaaktype: str
    registratiedatum: date
    startdatum: date
    einddatum: date | None
    omschrijving: str
    toelichting: str | None
    status: str | None
    identificatie: str
    bronorganisatie: str
    archiefstatus: str
    vertrouwelijkheidaanduiding: str
    verantwoordelijkeOrganisatie: str
