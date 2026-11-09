from flask import current_app, g
from backend.repositories import list_sleep, list_caffeine, list_exercise, list_screen
from backend.services.daily_features import build_daily_features


def db_session():
    return g.db


def load_daily_rows():
    session = db_session()
    return build_daily_features(
        list_sleep(session),
        list_caffeine(session),
        list_exercise(session),
        list_screen(session),
    )
