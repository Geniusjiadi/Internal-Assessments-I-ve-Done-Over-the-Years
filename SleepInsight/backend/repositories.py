from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .models import SleepRecord, CaffeineEvent, ExerciseSession, ScreenRecord, Goal
from .services.sleep_calculator import calculate_sleep_metrics


def sleep_to_dict(item: SleepRecord) -> dict:
    return {
        "id": item.id,
        "user_id": item.user_id,
        "sleep_date": item.sleep_date.isoformat(),
        "bedtime": item.bedtime,
        "wake_time": item.wake_time,
        "latency_minutes": item.latency_minutes,
        "awakenings": item.awakenings,
        "quality": item.quality,
        "notes": item.notes,
        "duration_minutes": item.duration_minutes,
        "sleep_midpoint_minutes": item.sleep_midpoint_minutes,
        "actual_sleep_start_iso": item.actual_sleep_start_iso,
    }


def caffeine_to_dict(item: CaffeineEvent) -> dict:
    return {
        "id": item.id, "event_date": item.event_date.isoformat(), "time": item.time,
        "amount_mg": item.amount_mg, "beverage_type": item.beverage_type,
    }


def exercise_to_dict(item: ExerciseSession) -> dict:
    return {
        "id": item.id, "event_date": item.event_date.isoformat(), "time": item.time,
        "duration_minutes": item.duration_minutes, "intensity": item.intensity,
    }


def screen_to_dict(item: ScreenRecord) -> dict:
    return {
        "id": item.id, "event_date": item.event_date.isoformat(),
        "total_minutes": item.total_minutes, "pre_bed_minutes": item.pre_bed_minutes,
    }


def goal_to_dict(item: Goal) -> dict:
    return {
        "id": item.id,
        "goal_type": item.goal_type,
        "title": item.title,
        "target_value": item.target_value,
        "target_time": item.target_time,
        "target_nights_per_week": item.target_nights_per_week,
        "start_date": item.start_date.isoformat(),
        "end_date": item.end_date.isoformat() if item.end_date else None,
        "active": item.active,
        "adaptive_enabled": item.adaptive_enabled,
    }


def list_sleep(session) -> list[dict]:
    items = session.scalars(select(SleepRecord).order_by(SleepRecord.sleep_date)).all()
    return [sleep_to_dict(i) for i in items]


def create_sleep(session, data: dict) -> dict:
    metrics = calculate_sleep_metrics(
        data["sleep_date"], data["bedtime"], data["wake_time"], data["latency_minutes"]
    )
    item = SleepRecord(user_id=1, **data, **metrics)
    session.add(item)
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("A sleep record already exists for this date") from exc
    return sleep_to_dict(item)


def update_sleep(session, item: SleepRecord, data: dict) -> dict:
    metrics = calculate_sleep_metrics(
        data["sleep_date"], data["bedtime"], data["wake_time"], data["latency_minutes"]
    )
    for key, value in {**data, **metrics}.items():
        setattr(item, key, value)
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("A sleep record already exists for this date") from exc
    return sleep_to_dict(item)


def get_sleep(session, record_id: int):
    return session.get(SleepRecord, record_id)


def delete_sleep(session, item: SleepRecord) -> None:
    session.delete(item)


def list_caffeine(session):
    return [caffeine_to_dict(i) for i in session.scalars(select(CaffeineEvent).order_by(CaffeineEvent.event_date, CaffeineEvent.time)).all()]


def create_caffeine(session, data):
    item = CaffeineEvent(user_id=1, **data)
    session.add(item); session.flush()
    return caffeine_to_dict(item)


def list_exercise(session):
    return [exercise_to_dict(i) for i in session.scalars(select(ExerciseSession).order_by(ExerciseSession.event_date, ExerciseSession.time)).all()]


def create_exercise(session, data):
    item = ExerciseSession(user_id=1, **data)
    session.add(item); session.flush()
    return exercise_to_dict(item)


def list_screen(session):
    return [screen_to_dict(i) for i in session.scalars(select(ScreenRecord).order_by(ScreenRecord.event_date)).all()]


def upsert_screen(session, data):
    item = session.scalar(select(ScreenRecord).where(ScreenRecord.event_date == data["event_date"]))
    if item is None:
        item = ScreenRecord(user_id=1, **data)
        session.add(item)
    else:
        item.total_minutes = data["total_minutes"]
        item.pre_bed_minutes = data["pre_bed_minutes"]
    session.flush()
    return screen_to_dict(item)


def list_goals(session):
    return [goal_to_dict(i) for i in session.scalars(select(Goal).order_by(Goal.created_at.desc())).all()]


def create_goal(session, data):
    item = Goal(user_id=1, **data)
    session.add(item); session.flush()
    return goal_to_dict(item)


def get_goal(session, goal_id):
    return session.get(Goal, goal_id)


def update_goal(session, item, data):
    for key, value in data.items():
        setattr(item, key, value)
    session.flush()
    return goal_to_dict(item)
