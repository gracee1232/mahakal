from sqlalchemy.orm import Session
from app.models import Translation
from app.hf_client import call_hf_translation
from app.sacred_terms import protect_sacred_terms, restore_sacred_terms
from app.concurrency import get_lock

async def translate_content(db: Session, content_id: int, title: str, desc: str, lang: str):

    existing = db.query(Translation).filter_by(
        content_id=content_id,
        language_code=lang
    ).first()

    if existing:
        return existing

    lock_key = f"{content_id}_{lang}"
    lock = get_lock(lock_key)

    async with lock:

        existing = db.query(Translation).filter_by(
            content_id=content_id,
            language_code=lang
        ).first()
        if existing:
            return existing

        title_protected = protect_sacred_terms(title)
        desc_protected = protect_sacred_terms(desc)

        translated_title = call_hf_translation(title_protected, lang)
        translated_desc = call_hf_translation(desc_protected, lang)

        translated_title = restore_sacred_terms(translated_title)
        translated_desc = restore_sacred_terms(translated_desc)

        new_translation = Translation(
            content_id=content_id,
            language_code=lang,
            translated_title=translated_title,
            translated_description=translated_desc
        )

        db.add(new_translation)
        db.commit()
        db.refresh(new_translation)

        return new_translation