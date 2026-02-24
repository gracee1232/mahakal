from pydantic import BaseModel

class TranslationRequest(BaseModel):
    content_id: int
    title_hindi: str
    description_hindi: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_title: str
    translated_description: str