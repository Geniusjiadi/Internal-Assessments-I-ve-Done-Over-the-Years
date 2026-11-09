import unittest
from datetime import date
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base, User
from backend.repositories import create_sleep, list_sleep
from backend.validators import validate_sleep_payload


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            future=True,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False, future=True)
        self.session = self.Session()
        self.session.add(User(id=1, display_name="Tester"))
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_sleep_persistence_and_duplicate_rejection(self):
        payload = validate_sleep_payload({
            "sleep_date":"2026-08-01","bedtime":"23:30","wake_time":"07:00",
            "latency_minutes":20,"awakenings":1,"quality":4
        })
        create_sleep(self.session, payload)
        self.session.commit()
        self.assertEqual(len(list_sleep(self.session)), 1)
        with self.assertRaises(ValueError):
            create_sleep(self.session, payload)


if __name__ == "__main__":
    unittest.main()
