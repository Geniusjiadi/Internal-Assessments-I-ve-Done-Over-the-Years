import os
import tempfile
import unittest

try:
    from backend.app import create_app
except ImportError:
    create_app = None


@unittest.skipIf(create_app is None, "Flask is not installed")
class ApiIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp.close()
        self.app = create_app({
            "TESTING": True,
            "DATABASE_URL": f"sqlite:///{self.temp.name}",
        })
        self.client = self.app.test_client()

    def tearDown(self):
        try:
            os.unlink(self.temp.name)
        except OSError:
            pass

    def test_health_and_sleep_crud(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)

        payload = {
            "sleep_date":"2026-08-01","bedtime":"23:30","wake_time":"07:00",
            "latency_minutes":20,"awakenings":1,"quality":4,"notes":"test"
        }
        created = self.client.post("/api/sleep", json=payload)
        self.assertEqual(created.status_code, 201)
        record_id = created.get_json()["id"]

        listed = self.client.get("/api/sleep")
        self.assertEqual(len(listed.get_json()), 1)

        payload["quality"] = 5
        updated = self.client.put(f"/api/sleep/{record_id}", json=payload)
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["quality"], 5)

        deleted = self.client.delete(f"/api/sleep/{record_id}")
        self.assertEqual(deleted.status_code, 200)

    def test_invalid_payload(self):
        bad = {
            "sleep_date":"2026-08-01","bedtime":"23:30","wake_time":"07:00",
            "latency_minutes":-4,"awakenings":0,"quality":4
        }
        self.assertEqual(self.client.post("/api/sleep", json=bad).status_code, 400)

    def test_analysis_endpoints(self):
        for endpoint in [
            "/api/dashboard",
            "/api/analytics/insights",
            "/api/analytics/trends?days=30",
            "/api/recommendations",
            "/api/goals",
        ]:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200, endpoint)

    def test_session_recovers_after_handled_400(self):
        payload = {
            "sleep_date":"2026-08-01","bedtime":"23:30","wake_time":"07:00",
            "latency_minutes":20,"awakenings":1,"quality":4,
        }
        self.assertEqual(self.client.post("/api/sleep", json=payload).status_code, 201)
        # Duplicate date -> 400; the request-scoped session's transaction has
        # already rolled back, so the next request must still work.
        duplicate = dict(payload, bedtime="22:30")
        self.assertEqual(self.client.post("/api/sleep", json=duplicate).status_code, 400)
        self.assertEqual(self.client.get("/api/sleep").status_code, 200)
        self.assertEqual(len(self.client.get("/api/sleep").get_json()), 1)


if __name__ == "__main__":
    unittest.main()
