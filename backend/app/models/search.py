from pydantic import BaseModel, Field


class SearchResults(BaseModel):
    name: str
    url: str


class FileSearchResult(SearchResults):
    name: str = Field(alias="title")
    url: str = Field(alias="resourceUrl")
