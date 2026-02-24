SACRED_MAP = {
    "महाकाल":     "__MAHAKAL__",
    "भस्म आरती":  "__BHASMA__",
    "ज्योतिर्लिंग": "__JYOTI__"
}

def protect_sacred_terms(text: str) -> str:
    for original, token in SACRED_MAP.items():
        text = text.replace(original, token)
    return text

def restore_sacred_terms(text: str) -> str:
    for original, token in SACRED_MAP.items():
        text = text.replace(token, original)
    return text