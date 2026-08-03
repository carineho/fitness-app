from sqlmodel import Session, select, func
from datetime import date, timedelta
from app.models import (
    Activity, ClimbSession, Climb,
    StrengthSession, Exercise,
    RunDetail, YogaDetail, DiveDetail,
)

def get_climbing_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, ClimbSession.gym, Climb.grade_raw, Climb.grade_normalized, Climb.attempts, Climb.sent)
        .join(ClimbSession, ClimbSession.activity_id == Activity.id)
        .join(Climb, Climb.climb_session_id == ClimbSession.id, isouter=True)
        .order_by(Activity.date)
    )
    results = session.exec(statement).all()
    return [
        {
            "date": row.date.isoformat(),
            "gym": row.gym,
            "grade_raw": row.grade_raw,
            "grade_normalized": row.grade_normalized,
            "attempts": row.attempts,
            "sent": row.sent,
        }
        for row in results
    ]


def get_climbing_by_gym(session: Session) -> list[dict]:
    statement = (
        select(
            ClimbSession.gym,
            func.count(Climb.id).label("total_climbs"),
            func.sum(func.cast(Climb.sent, int)).label("total_sends"),
            func.max(Climb.grade_normalized).label("max_grade"),
        )
        .join(Climb, Climb.climb_session_id == ClimbSession.id)
        .group_by(ClimbSession.gym)
    )
    results = session.exec(statement).all()
    return [
        {
            "gym": row.gym,
            "total_climbs": row.total_climbs,
            "total_sends": row.total_sends or 0,
            "max_grade": row.max_grade,
        }
        for row in results
    ]


def get_strength_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, StrengthSession.body_area, StrengthSession.id)
        .join(StrengthSession, StrengthSession.activity_id == Activity.id)
        .order_by(Activity.date)
    )
    results = session.exec(statement).all()
    return [
        {"date": row.date.isoformat(), "body_area": row.body_area, "strength_session_id": row.id}
        for row in results
    ]


def get_running_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, RunDetail.distance_km, RunDetail.pace_min_per_km)
        .join(RunDetail, RunDetail.activity_id == Activity.id)
        .order_by(Activity.date)
    )
    results = session.exec(statement).all()
    return [
        {"date": row.date.isoformat(), "distance_km": row.distance_km, "pace_min_per_km": row.pace_min_per_km}
        for row in results
    ]


def get_yoga_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, YogaDetail.yoga_type, YogaDetail.duration_minutes)
        .join(YogaDetail, YogaDetail.activity_id == Activity.id)
        .order_by(Activity.date)
    )
    results = session.exec(statement).all()
    return [
        {"date": row.date.isoformat(), "yoga_type": row.yoga_type, "duration_minutes": row.duration_minutes}
        for row in results
    ]


def get_diving_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, DiveDetail.dive_site, DiveDetail.duration_minutes, DiveDetail.max_depth_m)
        .join(DiveDetail, DiveDetail.activity_id == Activity.id)
        .order_by(Activity.date)
    )
    results = session.exec(statement).all()
    return [
        {
            "date": row.date.isoformat(),
            "dive_site": row.dive_site,
            "duration_minutes": row.duration_minutes,
            "max_depth_m": row.max_depth_m,
        }
        for row in results
    ]


def get_overview_stats(session: Session, days: int = 7) -> dict:
    cutoff = date.today() - timedelta(days=days)
    statement = (
        select(Activity.sport_type, func.count(Activity.id))
        .where(Activity.date >= cutoff)
        .group_by(Activity.sport_type)
    )
    results = session.exec(statement).all()
    by_sport = {sport: count for sport, count in results}
    return {
        "period_days": days,
        "total_sessions": sum(by_sport.values()),
        "by_sport": by_sport,
    }


def get_activities(session: Session, start_date: str = None, end_date: str = None, sport_type: str = None) -> list[dict]:
    statement = select(Activity)
    if start_date:
        statement = statement.where(Activity.date >= start_date)
    if end_date:
        statement = statement.where(Activity.date <= end_date)
    if sport_type:
        statement = statement.where(Activity.sport_type == sport_type)
    statement = statement.order_by(Activity.date)

    results = session.exec(statement).all()
    return [
        {"id": a.id, "date": a.date.isoformat(), "sport_type": a.sport_type, "notes": a.notes}
        for a in results
    ]