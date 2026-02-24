from huggingface_hub import InferenceClient
from app.config import HF_API_KEY

# Uses Mistral-7B via HF InferenceClient — zero local model loading.
# Confirmed working: translates Hindi to all Indic languages via LLM prompting.
client = InferenceClient(api_key=HF_API_KEY, timeout=120)

LANG_NAMES = {
    "en": "English",
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
    "as": "Assamese",
}


def call_hf_translation(text: str, target_lang: str) -> str:
    """
    Translate Hindi text to target_lang using Mistral-7B via HF Inference API.
    No local model loading — runs entirely on HF cloud infrastructure.
    """
    target_name = LANG_NAMES.get(target_lang, target_lang)

    prompt = (
        f"You are a highly accurate multilingual translation engine specialized in Indian religious content.\n\n"
        f"TASK:\n"
        f"Translate the COMPLETE Hindi input text into {target_name}.\n\n"
        f"CRITICAL RULES (MANDATORY):\n"
        f"1. Translate the FULL input text.\n"
        f"2. Do NOT drop any sentence.\n"
        f"3. Do NOT summarize.\n"
        f"4. Do NOT shorten.\n"
        f"5. Maintain the exact number of sentences as the input.\n"
        f"6. Preserve devotional tone.\n"
        f"7. Output only the translated text.\n"
        f"8. Do not add explanations.\n\n"
        f"SENTENCE INTEGRITY RULE:\n"
        f"If the input has N sentences, the output MUST also have N sentences.\n\n"
        f"SACRED TOKEN PROTECTION:\n"
        f"The following tokens must NEVER be translated or modified:\n"
        f"__MAHAKAL__\n"
        f"__BHASMA__\n"
        f"__JYOTI__\n\n"
        f"If these tokens appear in input, keep them EXACTLY unchanged in output.\n"
        f"Do NOT:\n"
        f"- Change spelling\n"
        f"- Translate them\n"
        f"- Add accents\n"
        f"- Modify casing\n\n"
        f"RELIGIOUS CONTEXT RULE:\n"
        f"Content refers to a Hindu temple and Lord Shiva.\n"
        f"Maintain respectful and devotional wording.\n\n"
        f"SOURCE LANGUAGE: Hindi\n"
        f"TARGET LANGUAGE: {target_name}\n\n"
        f"INPUT TEXT:\n{text}\n\n"
        f"OUTPUT:\n"
        f"(Only translated full text, same number of sentences, sacred tokens preserved)\n"
    )

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_tokens=512,
            temperature=0.1,
        )
        result = response.choices[0].message.content.strip()

        # Clean up any accidental prefix the model may add
        if ":" in result and len(result.split(":")[0]) < 25:
            result = result.split(":", 1)[-1].strip()
        result = result.strip('"').strip("'")

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Translation Error: {e}")
        raise e