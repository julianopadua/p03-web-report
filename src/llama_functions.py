from groq import Groq
import os
from utils import load_config

paths = load_config()

client = Groq(api_key=paths["groq"])


def translate_chart_labels(labels_dict, target_language="pt"):
    """
    Translates chart-related labels (title, axis labels) into the desired language using LLaMA.

    Args:
        labels_dict (dict): Dictionary with chart labels (e.g., {"title": "Stock Price", "x_axis": "Date"}).
        target_language (str): Target language code (e.g., "pt" for Portuguese).

    Returns:
        dict: Translated labels dictionary.
    """
    prompt = f"""
    You are a professional translator. Translate the following chart-related terms into {target_language},
    keeping them concise and appropriate for a financial chart:

    {labels_dict}

    Translated:
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=100,
            top_p=1,
            stream=False,
        )

        translated_text = completion.choices[0].message.content.strip()
        
        # Convert response back into a dictionary format
        translated_labels = eval(translated_text) if "{" in translated_text else {"error": "Invalid response"}
        
        return translated_labels

    except Exception as e:
        print(f"❌ Error contacting LLaMA: {e}")
        return labels_dict  # Fallback to original labels if translation fails

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
    labels = {
        "title": "AAPL Stock Price Over Time",
        "x_axis": "Date",
        "y_axis": "Closing Price (USD)"
    }

    translated_labels = translate_chart_labels(labels, target_language="pt")
    print(f"📊 Translated Labels: {translated_labels}")