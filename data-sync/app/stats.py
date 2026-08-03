from sqlmodel import Session, select
from app.models import Activity, ClimbSession, Climb

def get_climbing_stats(session: Session) -> list[dict]:
    statement = (
        select(Activity.date, ClimbSession.gym, Climb.grade_raw, Climb.grade_normalized, Climb.attempts, Climb.sent)
        .join(ClimbSession, ClimbSession.activity_id == Activity.id)
        .join(Climb, Climb.climb_session_id == ClimbSession.id)
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