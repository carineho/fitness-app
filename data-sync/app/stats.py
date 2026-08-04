from sqlmodel import Session, select, func
from datetime import date, timedelta
from app.models import (
    Activity,
    ClimbSession,
    Climb,
    StrengthSession,
    RunDetail,
    YogaDetail,
    DiveDetail,
)

def get_duration_stats(session: Session, sport_type: str = None) -> dict:
    statement = select(Activity.sport_type, Activity.duration_minutes).where(Activity.duration_minutes.is_not(None))
    if sport_type:
        statement = statement.where(Activity.sport_type == sport_type)

    results = session.exec(statement).all()
    if not results:
        return {"total_minutes": 0, "average_minutes": 0, "count": 0, "by_sport": {}}

    durations = [r.duration_minutes for r in results]
    by_sport = {}
    for sport, mins in results:
        by_sport.setdefault(sport, []).append(mins)

    return {
        "total_minutes": sum(durations),
        "average_minutes": round(sum(durations) / len(durations), 1),
        "count": len(durations),
        "by_sport": {
            sport: {"total_minutes": sum(vals), "average_minutes": round(sum(vals) / len(vals), 1), "count": len(vals)}
            for sport, vals in by_sport.items()
        },
    }

def get_weekly_summary(session: Session, days: int = 7) -> dict:
    cutoff = date.today() - timedelta(days=days)

    activities = session.exec(
        select(Activity).where(Activity.date >= cutoff)
    ).all()

    by_sport = {}
    total_duration = 0
    for a in activities:
        by_sport.setdefault(a.sport_type, []).append(a)
        if a.duration_minutes:
            total_duration += a.duration_minutes

    summary = {
        "period_days": days,
        "total_sessions": len(activities),
        "total_duration_minutes": total_duration,
        "by_sport": {sport: len(items) for sport, items in by_sport.items()},
    }

    # climbing detail: max grade, gyms visited
    climb_stats = get_climbing_stats(session)
    recent_climbs = [c for c in climb_stats if c["date"] >= cutoff.isoformat()]
    if recent_climbs:
        summary["climbing_detail"] = {
            "sessions": len(set(c["date"] for c in recent_climbs)),
            "gyms": list(set(c["gym"] for c in recent_climbs)),
            "max_grade": max((c["grade_normalized"] for c in recent_climbs if c["grade_normalized"]), default=None),
        }

    # strength detail: body areas trained
    strength_stats = get_strength_stats(session)
    recent_strength = [s for s in strength_stats if s["date"] >= cutoff.isoformat()]
    if recent_strength:
        summary["strength_detail"] = {
            "sessions": len(recent_strength),
            "body_areas": [s["body_area"] for s in recent_strength],
        }

    return summary

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
        select(Activity.date, Activity.duration_minutes, YogaDetail.yoga_type)
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
        select(Activity.date, Activity.duration_minutes, DiveDetail.dive_site, DiveDetail.max_depth_m)
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