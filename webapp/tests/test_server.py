import json
import sys
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import CyclingHandler, CyclingServer  # noqa: E402


class CyclingWebTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = CyclingServer(("127.0.0.1", 0), CyclingHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def json_request(self, path, payload=None, headers=None):
        body = json.dumps(payload).encode() if payload is not None else None
        request = Request(self.base + path, data=body, headers=headers or {})
        with urlopen(request, timeout=3) as response:
            return response.status, json.load(response), response.headers

    def test_health(self):
        status, body, headers = self.json_request("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")

    def test_home_page(self):
        with urlopen(self.base + "/", timeout=3) as response:
            html = response.read().decode()
        self.assertIn("Estymator testu", html)
        self.assertIn('name="viewport"', html)
        self.assertNotIn("athlete_id", html)

    def test_responsive_styles_have_desktop_tablet_and_phone_breakpoints(self):
        css = (Path(__file__).resolve().parents[1] / "static" / "styles.css").read_text()
        self.assertIn("@media (max-width: 980px)", css)
        self.assertIn("@media (max-width: 680px)", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_summary_contains_real_metrics_but_no_identifiers(self):
        _, body, _ = self.json_request("/api/summary")
        self.assertEqual(body["dataset"]["sessions"], 151399)
        self.assertFalse(body["methodology"]["saved_model_available"])
        self.assertNotIn("athlete_id", json.dumps(body))

    def test_interface_has_bilingual_controls_and_comparison_view(self):
        with urlopen(self.base + "/static/app.js", timeout=3) as response:
            javascript = response.read().decode()
        self.assertIn('localStorage.getItem("cycling-language")', javascript)
        self.assertIn('view: "Variant_B"', javascript)
        self.assertIn("Master's<br><em>thesis.</em>", javascript)

    def test_estimate(self):
        status, body, _ = self.json_request(
            "/api/estimate",
            {"mmp20": 286, "weight": 74},
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["ftp"], 271.7)
        self.assertEqual(body["watts_per_kg"], 3.67)

    def test_estimate_rejects_out_of_range_value(self):
        with self.assertRaises(HTTPError) as context:
            self.json_request(
                "/api/estimate",
                {"mmp20": 9999},
                {"Content-Type": "application/json"},
            )
        self.assertEqual(context.exception.code, 422)

    def test_estimate_errors_can_be_returned_in_english(self):
        request = Request(
            self.base + "/api/estimate",
            data=json.dumps({"mmp20": 9999, "lang": "en"}).encode(),
            headers={"Content-Type": "application/json", "Accept-Language": "en"},
        )
        with self.assertRaises(HTTPError) as context:
            urlopen(request, timeout=3)
        body = json.loads(context.exception.read())
        self.assertEqual(context.exception.code, 422)
        self.assertIn("must be between", body["error"])

    def test_predictions_are_anonymized(self):
        _, body, _ = self.json_request("/api/predictions?variant=Variant_B&limit=25")
        self.assertEqual(len(body["points"]), 25)
        self.assertEqual(set(body["points"][0]), {"actual", "predicted"})

    def test_rejects_unknown_variant(self):
        with self.assertRaises(HTTPError) as context:
            self.json_request("/api/predictions?variant=Variant_A")
        self.assertEqual(context.exception.code, 400)

    def test_thesis_pdf_supports_preview_download_and_ranges(self):
        with urlopen(self.base + "/thesis/INF.MN-152863-6350.pdf", timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers["Content-Type"], "application/pdf")
            self.assertIn("inline", response.headers["Content-Disposition"])
            self.assertGreater(int(response.headers["Content-Length"]), 3_000_000)
            self.assertEqual(response.read(4), b"%PDF")

        request = Request(self.base + "/thesis/INF.MN-152863-6350.pdf", headers={"Range": "bytes=0-99"})
        with urlopen(request, timeout=3) as response:
            self.assertEqual(response.status, 206)
            self.assertEqual(len(response.read()), 100)
            self.assertTrue(response.headers["Content-Range"].startswith("bytes 0-99/"))

        with urlopen(self.base + "/thesis/INF.MN-152863-6350.pdf?download=1", timeout=3) as response:
            self.assertIn("attachment", response.headers["Content-Disposition"])


if __name__ == "__main__":
    unittest.main()
