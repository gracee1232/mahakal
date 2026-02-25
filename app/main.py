from fastapi import FastAPI
from app.schemas import TranslationRequest, TranslationResponse
from app.translation_service import translate_content

app = FastAPI(title="Mahakal Translation Service")


@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    result = await translate_content(
        content_id=request.content_id,
        title=request.title_hindi,
        desc=request.description_hindi,
        lang=request.target_language,
    )
    return {
        "translated_title":       result["translated_title"],
        "translated_description": result["translated_description"],
    }