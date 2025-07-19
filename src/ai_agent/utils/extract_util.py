
import re
from dateutil.parser import parse as date_parse
from src.ai_agent.utils.ner_utils import extract_ner_entities
from src.ai_agent.utils.iata_codes import CITY_TO_IATA


def extract_entities_fallback(query: str):
    # City pattern: "from Delhi to Paris", "Delhi to Paris"
    city_matches = re.findall(r"(?:from\s+)?([A-Za-z\s]+?)\s+to\s+([A-Za-z\s]+)", query, re.IGNORECASE)
    cities = list(city_matches[0]) if city_matches else []

    # Date pattern: 17 March, 5 Jan
    date_matches = re.findall(
        r"\b\d{1,2}\s*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|"
        r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)\b", query, re.IGNORECASE)
    dates = date_matches

    return cities, dates


def extract_flight_details(query: str):
    """
    Extracts origin, destination, and travel_date from a user query.

    Returns:
        origin (str): IATA code or None
        destination (str): IATA code or None
        travel_date (str): YYYY-MM-DD or None
    """
    query = query.lower()

    ner_cities, ner_dates = extract_ner_entities(query)
    fallback_cities, fallback_dates = extract_entities_fallback(query)

    cities = fallback_cities if len(ner_cities) < 2 else ner_cities
    dates = fallback_dates if not ner_dates else ner_dates

    origin_city = cities[0].strip().lower() if len(cities) > 0 else None
    destination_city = cities[1].strip().lower() if len(cities) > 1 else None

    origin = CITY_TO_IATA.get(origin_city) if origin_city else None
    destination = CITY_TO_IATA.get(destination_city) if destination_city else None

    travel_date = None
    if dates:
        try:
            dt = date_parse(dates[0], fuzzy=True)
            travel_date = dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    print(f"🧠 Extracted flight details: origin={origin}, destination={destination}, date={travel_date}")
    return origin, destination, travel_date
