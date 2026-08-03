# sync.py
from sqlmodel import Session, select
from app.models import Activity, ClimbSession, StrengthSession, RunDetail, YogaDetail, DiveDetail

def upsert_activity(session: Session, fields: dict) -> Activity:
    existing = session.exec(
        select(Activity).where(Activity.notion_page_id == fields["notion_page_id"])
    ).first()

    if existing:
        existing.date = fields["date"]
        existing.sport_type = fields["sport_type"]
        existing.duration_minutes = fields["duration_min"]
        existing.notes = fields["notes"]
        activity = existing
    else:
        activity = Activity(
            notion_page_id=fields["notion_page_id"],
            date=fields["date"],
            sport_type=fields["sport_type"],
            duration_minutes=fields["duration_min"],
            notes=fields["notes"],
        )
        session.add(activity)

    session.commit()
    session.refresh(activity)
    return activity

def upsert_session_detail(session: Session, activity: Activity, fields: dict):
    sport = fields["sport_type"]

    if sport == "Climbing":
        existing = session.exec(
            select(ClimbSession).where(ClimbSession.activity_id == activity.id)
        ).first()
        if existing:
            existing.gym = fields["location"]
        else:
            session.add(ClimbSession(activity_id=activity.id, gym=fields["location"]))

    elif sport == "Strength":
        existing = session.exec(
            select(StrengthSession).where(StrengthSession.activity_id == activity.id)
        ).first()
        if existing:
            existing.body_area = ",".join(fields["body_area"])
        else:
            session.add(StrengthSession(activity_id=activity.id, body_area=",".join(fields["body_area"])))

    elif sport == "Running":
        existing = session.exec(
            select(RunDetail).where(RunDetail.activity_id == activity.id)
        ).first()
        if existing:
            existing.distance_km = fields["distance_km"]
            existing.pace_min_per_km = fields["pace"]
        else:
            session.add(RunDetail(activity_id=activity.id, distance_km=fields["distance_km"], pace_min_per_km=fields["pace"]))

    elif sport == "Yoga":
        existing = session.exec(
            select(YogaDetail).where(YogaDetail.activity_id == activity.id)
        ).first()
        if existing:
            existing.yoga_type = fields["yoga_type"]
        else:
            session.add(YogaDetail(activity_id=activity.id, yoga_type=fields["yoga_type"]))

    elif sport == "Diving":
        existing = session.exec(
            select(DiveDetail).where(DiveDetail.activity_id == activity.id)
        ).first()
        if existing:
            existing.dive_site = fields["dive_site"]
            existing.max_depth_m = fields["max_depth_m"]
        else:
            session.add(DiveDetail(activity_id=activity.id, dive_site=fields["dive_site"], max_depth_m=fields["max_depth_m"]))

    session.commit()

def sync_notion_to_db(session: Session, notion_pages: list[dict], mapper_fn):
    synced_count = 0
    skipped = []

    for page in notion_pages:
        try:
            fields = mapper_fn(page)

            if not fields["sport_type"]:
                skipped.append({"page_id": page["id"], "reason": "missing sport_type"})
                continue

            activity = upsert_activity(session, fields)
            upsert_session_detail(session, activity, fields)
            synced_count += 1

        except Exception as e:
            session.rollback()
            skipped.append({"page_id": page["id"], "reason": str(e)})

    return {"synced": synced_count, "skipped": skipped}