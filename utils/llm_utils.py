

def clean_text_paragraph(text):
    """
    Cleans a text paragraph by removing unnecessary blank lines
    and excessive indentation.
    """
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text