from app import json_store
from app.hf_client import call_hf_translation
from app.sacred_terms import protect_sacred_terms, restore_sacred_terms
from app.concurrency import get_lock


async def translate_content(
    content_id: int,
    title: str,
    desc: str,
    lang: str,
) -> dict:
    """
    Return a translation record (dict with translated_title / translated_description).

    Strategy:
      1. First look up the JSON cache (no lock needed for read).
      2. If found → return immediately (cache hit, no HF API call).
      3. Acquire a per-(content_id, lang) lock and check the cache again
         (double-checked locking to prevent duplicate API calls under concurrency).
      4. Call HF, persist via json_store.upsert(), return the record.
    """
    # ── 1. Fast path: cache hit ───────────────────────────────────────────────
    existing = json_store.lookup(content_id, lang)
    if existing:
        return existing

    # ── 2. Slow path: translate and cache ─────────────────────────────────────
    lock_key = f"{content_id}_{lang}"
    lock = get_lock(lock_key)

    async with lock:
        # Double-check after acquiring lock
        existing = json_store.lookup(content_id, lang)
        if existing:
            return existing

        title_protected = protect_sacred_terms(title)
        desc_protected  = protect_sacred_terms(desc)

        translated_title = call_hf_translation(title_protected, lang)
        translated_desc  = call_hf_translation(desc_protected,  lang)

        translated_title = restore_sacred_terms(translated_title)
        translated_desc  = restore_sacred_terms(translated_desc)

        record = json_store.upsert(
            content_id=content_id,
            lang=lang,
            translated_title=translated_title,
            translated_description=translated_desc,
        )
        return record