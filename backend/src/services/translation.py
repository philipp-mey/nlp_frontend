from easy_nlp_translate import initialize_translator


def translate(
    text: str,
    source_lang: str,
    target_lang: str,
    translator_name: str = "mbart",
) -> str:
    """
    Translate text from source language to target language using the specified translator.

    Args:
        text (str): The text to translate.
        source_lang (str): The source language code (e.g., "en" for English).
        target_lang (str): The target language code (e.g., "fr" for French).
        translator_name (str): The name of the translator to use (default is "mbart").
    Returns:
        str: The translated text.
    """

    translator = initialize_translator(
        translator_name=translator_name,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    translated_text = translator.translate(text=text)
    return translated_text
