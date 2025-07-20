
import spacy

# Load spaCy model once
_nlp = spacy.load("en_core_web_sm")

def extract_ner_entities(text: str):
    """
    Extracts city names (GPE, LOC) and date expressions from user query using spaCy NER.

    Args:
        text (str): User input.

    Returns:
        cities (list[str]): List of city/location names.
        dates (list[str]): List of date strings.
    """
    doc = _nlp(text.lower())
    cities = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    return cities, dates
