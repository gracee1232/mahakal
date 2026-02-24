import requests
import json
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

LANGUAGES = {
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "or": "Odia",
    "ur": "Urdu",
}

TITLE = "MAHAKAL मंदिर"
DESC  = "MAHAKAL मंदिर उज्जैन में स्थित है। यहाँ प्रतिदिन BHASMA आरती होती है। JYOTI की रोशनी से पूरा मंदिर प्रकाशित होता है।"

print("=" * 65)
print("Live API Test — All 10 Indic Languages")
print(f"Title : {TITLE}")
print(f"Desc  : {DESC}")
print("=" * 65)

passed = 0
failed = 0

for i, (code, name) in enumerate(LANGUAGES.items(), start=20):
    payload = {
        "content_id": i,
        "title_hindi": TITLE,
        "description_hindi": DESC,
        "target_language": code
    }
    try:
        r = requests.post("http://localhost:8000/translate", json=payload, timeout=150)
        if r.status_code == 200:
            data = r.json()
            print(f"\n[PASS] {name} ({code})")
            print(f"  Title : {data['translated_title']}")
            print(f"  Desc  : {data['translated_description']}")
            passed += 1
        else:
            print(f"\n[FAIL] {name} ({code}) -> HTTP {r.status_code}: {r.text[:120]}")
            failed += 1
    except Exception as e:
        print(f"\n[FAIL] {name} ({code}) -> {e}")
        failed += 1

print("\n" + "=" * 65)
print(f"Results: {passed} passed, {failed} failed out of {len(LANGUAGES)}")
print("=" * 65)
