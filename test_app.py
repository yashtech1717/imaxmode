import io
import os
import unittest
from unittest.mock import patch, MagicMock

# Set test mode so startup won't crash on unconfigured local dev environment
os.environ["TEST_MODE"] = "1"

import db
import cloud_storage
from fastapi.testclient import TestClient
from main import app


class TestStrictCloudArchitecture(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_strict_db_refuses_when_unconfigured(self):
        """Verifies db.get_connection() raises RuntimeError when DATABASE_URL is not set so app never uses SQLite."""
        with patch.dict(os.environ, {"DATABASE_URL": ""}, clear=False):
            with self.assertRaises(RuntimeError) as ctx:
                db.get_connection()
            self.assertIn("DATABASE_URL environment variable is missing", str(ctx.exception))

    def test_strict_storage_refuses_when_unconfigured(self):
        """Verifies cloud_storage.upload_file() raises HTTPException(500) and NEVER writes locally."""
        with patch.dict(os.environ, {"SUPABASE_URL": "", "SUPABASE_KEY": ""}, clear=False):
            from fastapi import HTTPException
            with self.assertRaises(HTTPException) as ctx:
                cloud_storage.upload_file(b"fake data", "test.png")
            self.assertEqual(ctx.exception.status_code, 500)
            self.assertIn("Supabase Cloud Storage is not configured", ctx.exception.detail)

    def test_health_endpoints_report_supabase(self):
        """Verifies both /health and /api/health report storage_mode as 'supabase'."""
        for endpoint in ["/health", "/api/health"]:
            res = self.client.get(endpoint)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("status", data)
            self.assertEqual(data["storage_mode"], "supabase")
            self.assertIn("database", data)
            self.assertIn("storage", data)

    def test_auth_admin_success(self):
        res = self.client.post("/api/login", json={"username": "yash", "password": "yashadmin17"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["role"], "admin")
        self.assertEqual(data["username"], "yash")

    def test_auth_viewer_variants(self):
        # Test lowercase
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

    def test_api_html_home(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("<!DOCTYPE html>", res.text)

    def test_admin_upload_cloud_success(self):
        """Verifies successful upload returns a public cloud CDN URL."""
        mock_upload_result = {
            "url": "https://mock-project.supabase.co/storage/v1/object/public/memories/test.jpg",
            "media_type": "image",
            "filename": "test.jpg",
            "is_cloud": True,
            "storage": "supabase"
        }
        with patch("main.upload_file", return_value=mock_upload_result):
            file_data = io.BytesIO(b"fake image data")
            file_data.name = "test.jpg"
            res = self.client.post(
                "/api/admin/upload",
                files={"file": ("test.jpg", file_data, "image/jpeg")}
            )
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["url"], mock_upload_result["url"])
            self.assertEqual(data["is_cloud"], True)
            self.assertTrue(data["url"].startswith("https://"))


class TestMockedCloudEndpoints(unittest.TestCase):
    """Verifies content, config, chapters, and replies API routes using mock DB layer."""
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.get_site_config")
    @patch("main.get_chapters")
    def test_content_delivery(self, mock_get_chapters, mock_get_config):
        mock_get_config.return_value = {
            "id": 1,
            "headline_word1": "HAPPY",
            "headline_word2": "BIRTHDAY",
            "giant_word": "YASH"
        }
        mock_get_chapters.return_value = [
            {"step_index": 0, "title": "THE VISIONARY", "badge": "// CHAPTER 01", "counter": "01 / 04"}
        ]
        res = self.client.get("/api/content")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["config"]["giant_word"], "YASH")
        self.assertEqual(len(data["chapters"]), 1)

    @patch("main.update_site_config")
    def test_admin_config_update(self, mock_update_config):
        mock_update_config.return_value = {
            "id": 1,
            "headline_word1": "HAPPY",
            "giant_word": "YASH_UPDATED"
        }
        res = self.client.post("/api/admin/config", json={"giant_word": "YASH_UPDATED"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["giant_word"], "YASH_UPDATED")

    @patch("main.update_chapter")
    def test_admin_chapter_update(self, mock_update_chapter):
        mock_update_chapter.return_value = {
            "step_index": 0,
            "title": "UPDATED TITLE"
        }
        res = self.client.post("/api/admin/chapter", json={
            "step_index": 0,
            "title": "UPDATED TITLE"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["title"], "UPDATED TITLE")

    @patch("main.add_reply")
    def test_viewer_reply(self, mock_add_reply):
        mock_add_reply.return_value = {
            "id": 1,
            "sender": "Glory",
            "message": "Happy Birthday Yash!",
            "chapter_index": 0,
            "chapter_title": "THE VISIONARY"
        }
        res = self.client.post("/api/viewer/reply", json={
            "sender": "Glory",
            "message": "Happy Birthday Yash!",
            "chapter_index": 0,
            "chapter_title": "THE VISIONARY"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["sender"], "Glory")

    @patch("main.get_replies")
    def test_admin_fetch_replies(self, mock_get_replies):
        mock_get_replies.return_value = [
            {"id": 1, "sender": "Glory", "message": "Best wishes!", "created_at": "2026-09-17T16:00:00"}
        ]
        res = self.client.get("/api/admin/replies")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 1)

    @patch("main.delete_reply")
    def test_admin_delete_reply(self, mock_delete_reply):
        mock_delete_reply.return_value = True
        res = self.client.delete("/api/admin/reply/1")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        mock_delete_reply.assert_called_once_with(1)

    @patch("main.delete_all_replies")
    def test_admin_clear_replies(self, mock_clear_replies):
        mock_clear_replies.return_value = True
        res = self.client.delete("/api/admin/replies/clear")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        mock_clear_replies.assert_called_once()

    @patch("main.clear_login_logs")
    def test_admin_clear_login_logs(self, mock_clear_logs):
        mock_clear_logs.return_value = True
        res = self.client.delete("/api/admin/login-logs")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        mock_clear_logs.assert_called_once()

    @patch("main.get_login_logs")
    def test_admin_fetch_login_logs(self, mock_get_login_logs):
        mock_get_login_logs.return_value = [
            {
                "id": 1,
                "username": "yash",
                "role": "admin",
                "ip_address": "127.0.0.1",
                "user_agent": "Mozilla/5.0",
                "created_at": "2026-09-19T07:00:00"
            }
        ]
        res = self.client.get("/api/admin/login-logs")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["username"], "yash")
        self.assertEqual(data["data"][0]["role"], "admin")

    @patch("main.record_login")
    def test_login_records_audit_log(self, mock_record_login):
        res = self.client.post(
            "/api/login",
            json={"username": "yash", "password": "yashadmin17"},
            headers={"User-Agent": "TestBrowser/1.0", "X-Forwarded-For": "203.0.113.195"}
        )
        self.assertEqual(res.status_code, 200)
        mock_record_login.assert_called_once_with(
            "yash",
            "admin",
            "203.0.113.195",
            "TestBrowser/1.0"
        )

    @patch("main.get_active_feedback_question")
    def test_active_feedback_question(self, mock_active_q):
        mock_active_q.return_value = {
            "id": 1,
            "question": "How did you find this surprise?",
            "is_active": True
        }
        res = self.client.get("/api/feedback/active-question")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["question"], "How did you find this surprise?")

    @patch("main.submit_feedback")
    def test_submit_feedback_success(self, mock_submit_fb):
        mock_submit_fb.return_value = {
            "id": 1,
            "question_id": 1,
            "question_text": "How did you find this surprise?",
            "sender": "Glory",
            "rating": 5,
            "comment": "Unbelievable masterpiece!"
        }
        res = self.client.post("/api/feedback/submit", json={
            "question_id": 1,
            "question_text": "How did you find this surprise?",
            "sender": "Glory",
            "rating": 5,
            "comment": "Unbelievable masterpiece!"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["rating"], 5)

    @patch("main.get_feedback_responses")
    @patch("main.get_feedback_stats")
    @patch("main.get_all_feedback_questions")
    @patch("main.get_active_feedback_question")
    def test_admin_fetch_feedback(self, mock_act_q, mock_all_q, mock_stats, mock_resps):
        mock_act_q.return_value = {"id": 1, "question": "Active Q"}
        mock_all_q.return_value = [{"id": 1, "question": "Active Q"}]
        mock_stats.return_value = {"total_count": 1, "average_rating": 5.0, "breakdown": {5: 1}}
        mock_resps.return_value = [
            {"id": 1, "question_id": 1, "sender": "Glory", "rating": 5, "comment": "Loved it"}
        ]
        res = self.client.get("/api/admin/feedback")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["stats"]["average_rating"], 5.0)
        self.assertEqual(len(data["responses"]), 1)

    @patch("main.create_feedback_question")
    def test_admin_create_feedback_question(self, mock_create_q):
        mock_create_q.return_value = {
            "id": 2,
            "question": "What was your favorite chapter?",
            "is_active": True
        }
        res = self.client.post("/api/admin/feedback/question", json={
            "question": "What was your favorite chapter?"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["question"], "What was your favorite chapter?")



    @patch("main.reorder_chapter")
    def test_reorder_chapter_endpoint(self, mock_reorder):
        mock_reorder.return_value = [
            {"step_index": 0, "title": "CHAPTER 01", "counter": "01 / 04"},
            {"step_index": 1, "title": "CHAPTER 03", "counter": "02 / 04"},
            {"step_index": 2, "title": "CHAPTER 02", "counter": "03 / 04"},
            {"step_index": 3, "title": "CHAPTER 04", "counter": "04 / 04"},
        ]
        res = self.client.post("/api/admin/chapter/reorder", json={"from_index": 1, "to_index": 2})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["from_index"], 1)
        self.assertEqual(data["to_index"], 2)
        self.assertEqual(len(data["chapters"]), 4)
        mock_reorder.assert_called_once_with(1, 2)

    def test_reorder_chapter_invalid_index(self):
        res = self.client.post("/api/admin/chapter/reorder", json={"from_index": -1, "to_index": 2})
        self.assertEqual(res.status_code, 400)

    def test_diagnostic_endpoints(self):
        # Test HTML view
        res_html = self.client.get("/diagnostic", headers={"Accept": "text/html"})
        self.assertEqual(res_html.status_code, 200)
        self.assertIn("Supabase 7-Point Diagnostic Report", res_html.text)

        # Test API JSON view
        res_json = self.client.get("/api/diagnostic")
        self.assertEqual(res_json.status_code, 200)
        data = res_json.json()
        self.assertIn("supabase_url", data)
        self.assertIn("supabase_key", data)
        self.assertIn("supabase_client", data)
        self.assertIn("supabase_authentication", data)
        self.assertIn("postgres_connection", data)
        self.assertIn("database_schema", data)
        self.assertIn("storage_bucket", data)

    def test_media_stream_missing_parameter(self):
        res = self.client.get("/api/media/stream")
        self.assertEqual(res.status_code, 400)
        self.assertIn("Missing media", res.json()["detail"])

    @patch("main.get_storage_stream_info")
    def test_media_stream_head(self, mock_stream_info):
        mock_stream_info.return_value = (
            200,
            {"content-type": "video/mp4", "content-length": "2048000"},
            None
        )
        res = self.client.head("/api/media/stream?url=https://supabase.co/storage/v1/object/public/memories/test.mp4")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("accept-ranges"), "bytes")
        self.assertEqual(res.headers.get("content-type"), "video/mp4")
        self.assertEqual(res.headers.get("content-length"), "2048000")

    @patch("main.get_storage_stream_info")
    def test_media_stream_range_206(self, mock_stream_info):
        class DummyStream:
            def iter_content(self, chunk_size=65536):
                yield b"A" * 1000
            def close(self):
                pass

        mock_stream_info.return_value = (
            206,
            {
                "content-type": "video/mp4",
                "content-length": "1000",
                "content-range": "bytes 0-999/2048000"
            },
            DummyStream()
        )
        res = self.client.get(
            "/api/media/stream/memories/test.mp4",
            headers={"Range": "bytes=0-999"}
        )
        self.assertEqual(res.status_code, 206)
        self.assertEqual(res.headers.get("accept-ranges"), "bytes")
        self.assertEqual(res.headers.get("content-range"), "bytes 0-999/2048000")
        self.assertEqual(len(res.content), 1000)


if __name__ == "__main__":
    unittest.main()
