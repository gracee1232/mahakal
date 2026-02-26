from huggingface_hub import InferenceClient
from app.config import HF_API_KEY

# Zero local model loading — runs entirely on HF cloud infrastructure.
client = InferenceClient(api_key=HF_API_KEY, timeout=120)

LANG_NAMES = {
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "kn": "Kannada",
    "gu": "Gujarati",
    "bn": "Bengali",
}


def call_hf_translation(text: str, target_lang: str) -> str:
    """
    Translate Hindi text to target_lang using Llama-3.1-8B via HF Inference API.
    Restricted to 3 Indic languages: Gujarati, Bengali, and Kannada.
    """
    target_name = LANG_NAMES.get(target_lang, target_lang)

    prompt = (
        f"Translate the following Hindi text into {target_name}.\n"
        f"Rules:\n"
        f"1. Output ONLY the translated text in {target_name} script.\n"
        f"2. Do NOT translate or modify these tokens: __MAHAKAL__, __BHASMA__, __JYOTI__.\n"
        f"3. Maintain the same number of sentences.\n"
        f"4. Source: Hindi. Target: {target_name}.\n\n"
        f"Text: {text}\n"
        f"Translation:"
    )

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=512,
            temperature=0.1,
        )
        result = response.choices[0].message.content.strip()

        # Clean up any accidental prefix
        if ":" in result and len(result.split(":")[0]) < 20:
            result = result.split(":", 1)[-1].strip()
        result = result.strip('"').strip("'")

        return result

    except Exception as e:
        print(f"Translation Error: {e}")
        raise e