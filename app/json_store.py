"""
json_store.py
─────────────
Lightweight file-based JSON persistence replacing SQLAlchemy/SQLite.

Layout of translated_output.json:
{
    "<content_id>_<lang>": {
        "content_id": int,
        "language_code": str,
        "translated_title": str,
        "translated_description": str
    },
    ...
}
"""

import json
import os
import tempfile

from app.config import OUTPUT_FILE


# ── helpers ──────────────────────────────────────────────────────────────────

def _make_key(content_id: int, lang: str) -> str:
    return f"{content_id}_{lang}"


def load_output() -> dict:
    """Return the full translation cache, or {} if the file doesn't exist yet."""
    if not os.path.exists(OUTPUT_FILE):
        return {}
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_output(data: dict) -> None:
    """Atomically write *data* to OUTPUT_FILE using a temp-file + os.replace."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    dir_name = os.path.dirname(OUTPUT_FILE)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=dir_name,
        delete=False,
        suffix=".tmp",
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, OUTPUT_FILE)


# ── public API ────────────────────────────────────────────────────────────────

def lookup(content_id: int, lang: str) -> dict | None:
    """Return a cached translation record, or None if not found."""
    data = load_output()
    return data.get(_make_key(content_id, lang))


def upsert(content_id: int, lang: str, translated_title: str, translated_description: str) -> dict:
    """
    Insert or update a translation record and persist atomically.
    Returns the stored record dict.
    """
    record = {
        "content_id": content_id,
        "language_code": lang,
        "translated_title": translated_title,
        "translated_description": translated_description,
    }
    data = load_output()
    data[_make_key(content_id, lang)] = record
    save_output(data)
    return record
