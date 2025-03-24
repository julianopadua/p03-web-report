from groq import Groq
import os
from utils import load_config

paths = load_config()

client = Groq(api_key=paths["groq"])

def translate_date(date_str, target_language="pt"):
    """
    Ask LLaMA to translate a date into the desired language.

    Args:
        date_str (str): A formatted date in English (e.g., "March 24, 2025").
        target_language (str): Target language code (e.g., "pt" for Portuguese).

    Returns:
        str: Translated date in the target language.
    """
    prompt = f"""
    You are an expert translator. Translate the following date into {target_language}, maintaining natural date formatting:

    English: {date_str}
    Translated:
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=50,
            top_p=1,
            stream=False,
        )

        translated_date = completion.choices[0].message.content.strip()
        return translated_date

    except Exception as e:
        print(f"❌ Error contacting LLaMA: {e}")
        return date_str  # Fallback to original date if translation fails

# Example usage
if __name__ == "__main__":
    date_en = "March 24, 2025"
    
    # Translate to Portuguese
    date_pt = translate_date(date_en, target_language="pt")
    print(f"📅 Translated Date (PT): {date_pt}")

    # Translate to Spanish
    date_es = translate_date(date_en, target_language="french")
    print(f"📅 Translated Date (ES): {date_es}")