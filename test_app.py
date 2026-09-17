import unittest
import io
import os
import db
from fastapi.testclient import TestClient
from main import app

class TestCinematicPortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init_db()
        cls.client = TestClient(app)

    def test_auth_admin_success(self):
        res = self.client.post("/api/login", json={"username": "yash", "password": "yashadmin17"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["role"], "admin")
        self.assertEqual(data["username"], "yash")

    def test_auth_viewer_variants(self):
        # Test lower case
        res1 = self.client.post("/api/login", json={"username": "glory", "password": "lory"})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.json()["role"], "viewer")

        # Test Title case
        res2 = self.client.post("/api/login", json={"username": "Glory", "password": "Lory"})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()["role"], "viewer")

    def test_auth_invalid(self):
        res = self.client.post("/api/login", json={"username": "wrong", "password": "wrong"})
        self.assertEqual(res.status_code, 401)

    def test_content_delivery(self):
        res = self.client.get("/api/content")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("config", data)
        self.assertIn("chapters", data)
        self.assertGreaterEqual(len(data["chapters"]), 4)

    def test_admin_config_update(self):
        res = self.client.post("/api/admin/config", json={
            "giant_word": "YASH_TEST",
            "top_badge": "TEST BADGE"
        })
        self.assertEqual(res.status_code, 200)
        config = res.json()["data"]
        self.assertEqual(config["giant_word"], "YASH_TEST")

        # Restore
        self.client.post("/api/admin/config", json={"giant_word": "YASH", "top_badge": "NEXT LEVEL UI / UX"})

    def test_admin_chapter_update(self):
        res = self.client.post("/api/admin/chapter", json={
            "step_index": 0,
            "title": "UPDATED VISIONARY",
            "body": "Updated body text for chapter 1."
        })
        self.assertEqual(res.status_code, 200)
        chapter = res.json()["data"]
        self.assertEqual(chapter["title"], "UPDATED VISIONARY")

        # Restore
        self.client.post("/api/admin/chapter", json={
            "step_index": 0,
            "title": "THE VISIONARY",
            "body": "Every masterpiece begins with bold vision. Your creativity, relentless drive, and dedication to excellence transform ideas into reality. Keep dreaming big, YASH."
        })

    def test_admin_upload_local_fallback(self):
        file_data = io.BytesIO(b"fake image data")
        file_data.name = "sample_test_photo.jpg"
        res = self.client.post(
            "/api/admin/upload",
            files={"file": ("sample_test_photo.jpg", file_data, "image/jpeg")}
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["media_type"], "image")
        self.assertTrue(data["url"].startswith("/static/uploads/") or data["url"].startswith("https://"))
        self.assertIn("is_cloud", data)

    def test_admin_chapter_add_and_delete(self):
        # Fetch initial count
        init_res = self.client.get("/api/content")
        init_count = len(init_res.json()["chapters"])

        # Add chapter
        add_res = self.client.post("/api/admin/chapter/add")
        self.assertEqual(add_res.status_code, 200)
        data = add_res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["chapters"]), init_count + 1)
        new_step_idx = init_count

        # Verify added chapter counter format e.g. "05 / 05"
        last_chapter = data["chapters"][-1]
        self.assertEqual(last_chapter["step_index"], new_step_idx)

        # Delete the added chapter
        del_res = self.client.delete(f"/api/admin/chapter/{new_step_idx}")
        self.assertEqual(del_res.status_code, 200)
        del_data = del_res.json()
        self.assertEqual(del_data["status"], "success")
        self.assertEqual(len(del_data["chapters"]), init_count)

    def test_viewer_reply_with_chapter_context(self):
        # Glory sends a reply tagged with chapter 1
        reply_res = self.client.post("/api/viewer/reply", json={
            "sender": "Glory",
            "message": "Loved this specific memory!",
            "chapter_index": 0,
            "chapter_title": "THE VISIONARY"
        })
        self.assertEqual(reply_res.status_code, 200)
        reply = reply_res.json()["data"]
        self.assertEqual(reply["sender"], "Glory")
        self.assertEqual(reply["chapter_index"], 0)
        self.assertEqual(reply["chapter_title"], "THE VISIONARY")

        # Yash reads replies and verifies left-join on chapter fields
        inbox_res = self.client.get("/api/admin/replies")
        self.assertEqual(inbox_res.status_code, 200)
        replies = inbox_res.json()["data"]
        matching = [r for r in replies if r.get("message") == "Loved this specific memory!"]
        self.assertTrue(len(matching) > 0)
        self.assertEqual(matching[0]["chapter_index"], 0)
        self.assertEqual(matching[0]["chapter_title"], "THE VISIONARY")

    def test_api_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("database", data)
        self.assertIn("cloud_storage", data)

    def test_api_html_home(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("<!DOCTYPE html>", res.text)

if __name__ == "__main__":
    unittest.main()

