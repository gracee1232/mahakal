from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.schemas import TranslationRequest, TranslationResponse
from app.translation_service import translate_content

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest, db: Session = Depends(get_db)):

    result = await translate_content(
        db,
        request.content_id,
        request.title_hindi,
        request.description_hindi,
        request.target_language
    )

    return {
        "translated_title": result.translated_title,
        "translated_description": result.translated_description
    }