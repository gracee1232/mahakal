"""
Test IndicTrans2 via HF Inference API for all supported Indic languages.
No local model loading - purely API based.
"""
import sys
import os

# Fix encoding for Windows terminal
os.environ["PYTHONIOENCODING"] = "utf-8"

from app.hf_client import call_hf_translation

TEST_HINDI = "महाकाल मंदिर उज्जैन में स्थित है। यह भगवान शिव का पवित्र धाम है।"

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

def run_tests():
    print("=" * 60)
    print("IndicTrans2 API Translation Test")
    print("Source (Hindi):", TEST_HINDI)
    print("=" * 60)

    passed = 0
    failed = 0

    for code, name in LANGUAGES.items():
        try:
            result = call_hf_translation(TEST_HINDI, code)
            print(f"\n[PASS] {name} ({code}):")
            print(f"  {result}")
            passed += 1
        except Exception as e:
            print(f"\n[FAIL] {name} ({code}): {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(LANGUAGES)} languages")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
