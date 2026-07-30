# to extract values from notion database
from app.constants import NOTION_PROPERTY_NAMES

TITLE = "title"
PLAIN_TEXT = "plain_text"
RICH_TEXT = "rich_text"
NAME = "name"
START = "start"
SELECT = "select"
MULTI_SELECT = "multi_select"
NUMBER = "number"
CHECKBOX = "checkbox"


def get_property_name(key: str) -> str:
    return NOTION_PROPERTY_NAMES.get(key, key)

def get_title(properties: dict, key: str) -> str:
    items = properties[key][TITLE]
    return items[0][PLAIN_TEXT] if items else ""

def get_rich_text(properties: dict, key: str) -> str:
    items = properties[key][RICH_TEXT]
    return items[0][PLAIN_TEXT] if items else ""

def get_select(properties: dict, key: str) -> str | None:
    select = properties[key][SELECT]
    return select[NAME] if select else None

def get_multi_select(properties: dict, key: str) -> list[str]:
    return [item[NAME] for item in properties[key][MULTI_SELECT]]

def get_date(properties: dict, key: str) -> str | None:
    date_obj = properties[key]["date"]
    return date_obj[START] if date_obj else None

def get_number(properties: dict, key: str) -> float | None:
    return properties[key][NUMBER]

def get_checkbox(properties: dict, key: str) -> bool:
    return properties[key][CHECKBOX]

def map_page_to_activity_fields(page: dict) -> dict:
    props = page["properties"]
    return {
        "notion_page_id": page["id"],
        "name": get_title(props, get_property_name("name")),
        "date": get_date(props, get_property_name("date")),
        "sport_type": get_select(props, get_property_name("sport_type")),
        "body_area": get_multi_select(props, get_property_name("body_area")),
        "location": get_rich_text(props, get_property_name("location")),
        "distance_km": get_number(props, get_property_name("distance_km")),
        "pace": get_number(props, get_property_name("pace")),
        "yoga_type": get_select(props, get_property_name("yoga_type")),
        "dive_site": get_rich_text(props, get_property_name("dive_site")),
        "max_depth_m": get_number(props, get_property_name("max_depth_m")),
        "duration_min": get_number(props, get_property_name("duration_min")),
        "details": get_rich_text(props, get_property_name("details")),
        "notes": get_rich_text(props, get_property_name("notes")),
        "synced": get_checkbox(props, get_property_name("synced")),
    }