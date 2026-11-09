from __future__ import annotations

from datetime import date, timedelta, datetime
import random
from sqlalchemy import delete

from .config import Config
from .db import Database
from .models import SleepRecord, CaffeineEvent, ExerciseSession, ScreenRecord, Goal
from .repositories import create_sleep
from .services.sleep_calculator import minutes_to_hhmm


def seed_database(days: int = 75):
    random.seed(21)
    db = Database(Config.DATABASE_URL)
    db.create_all()
    start = date.today() - timedelta(days=days - 1)

    with db.session_scope() as session:
        for model in [SleepRecord, CaffeineEvent, ExerciseSession, ScreenRecord, Goal]:
            session.execute(delete(model))

        for i in range(days):
            d = start + timedelta(days=i)
            weekend = d.weekday() >= 5
            base_bed = 23 * 60 + 20 + (70 if weekend else 0)
            screen = max(10, int(random.gauss(55 if not weekend else 85, 22)))
            bedtime_min = (base_bed + int(screen * 0.18) + random.randint(-25, 25)) % 1440
            late_caff = random.random() < (0.38 if i % 3 == 0 else 0.20)
            caffeine_mg = random.choice([70, 90, 120]) if late_caff else 0
            latency = max(5, int(random.gauss(17 + screen * 0.10 + caffeine_mg * 0.07, 8)))
            wake_min = (7 * 60 + 10 + (75 if weekend else 0) + random.randint(-20, 20)) % 1440
            quality = max(1, min(5, round(5.1 - screen / 55 - caffeine_mg / 110 + random.uniform(-0.5, 0.5))))
            bed_time = minutes_to_hhmm(bedtime_min)
            wake_time = minutes_to_hhmm(wake_min)

            data = {
                "sleep_date": d,
                "bedtime": bed_time,
                "wake_time": wake_time,
                "latency_minutes": latency,
                "awakenings": random.choice([0, 0, 1, 1, 2]),
                "quality": quality,
                "notes": None,
            }
            try:
                create_sleep(session, data)
            except ValueError:
                continue

            session.add(ScreenRecord(
                user_id=1, event_date=d,
                total_minutes=screen + random.randint(180, 340),
                pre_bed_minutes=screen,
            ))

            if random.random() < 0.80:
                session.add(CaffeineEvent(
                    user_id=1, event_date=d,
                    time="16:30" if late_caff else "09:10",
                    amount_mg=caffeine_mg if late_caff else random.choice([60, 80, 100]),
                    beverage_type="Coffee",
                ))

            if random.random() < 0.62:
                session.add(ExerciseSession(
                    user_id=1, event_date=d, time="17:30",
                    duration_minutes=random.choice([20, 30, 45, 60]),
                    intensity=random.choice(["Low", "Moderate", "High"]),
                ))

        session.add(Goal(
            user_id=1,
            goal_type="bedtime_before",
            title="Sleep before 23:45",
            target_time="23:45",
            target_nights_per_week=5,
            start_date=start,
            active=True,
            adaptive_enabled=True,
        ))
        session.add(Goal(
            user_id=1,
            goal_type="prebed_screen_max",
            title="Keep pre-bed screen time at or below 45 minutes",
            target_value=45,
            target_nights_per_week=5,
            start_date=start,
            active=True,
            adaptive_enabled=True,
        ))

    print(f"Seeded {days} days into {Config.DATABASE_URL}")


if __name__ == "__main__":
    seed_database()
