# to extract values from notion database

TITLE = "title"
PLAIN_TEXT = "plain_text"
RICH_TEXT = "rich_text"
NAME = "name"
START = "start"
SELECT = "select"
MULTI_SELECT = "multi_select"
NUMBER = "number"
CHECKBOX = "checkbox"

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
        "name": get_title(props, "Name"),
        "date": get_date(props, "Date"),
        "sport_type": get_select(props, "Sport Type"),
        "body_area": get_multi_select(props, "Body Area"),
        "location": get_rich_text(props, "Location"),
        "distance_km": get_number(props, "Distance (km)"),
        "pace": get_number(props, "Pace (min/km)"),
        "yoga_type": get_select(props, "Yoga Type"),
        "dive_site": get_rich_text(props, "Dive Site"),
        "max_depth_m": get_number(props, "Max Depth (m)"),
        "duration_min": get_number(props, "Duration (min)"),
        "details": get_rich_text(props, "Details"),
        "notes": get_rich_text(props, "Notes"),
        "synced": get_checkbox(props, "Synced"),
    }