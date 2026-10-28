import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server as server_module  # noqa: E402
from server import CyclingHandler, CyclingServer  # noqa: E402


class CyclingWebTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader_assets = tempfile.TemporaryDirectory()
        reader_root = Path(cls.reader_assets.name)
        (reader_root / "page-01.jpg").write_bytes(b"\xff\xd8page-one\xff\xd9")
        (reader_root / "page-02.jpg").write_bytes(b"\xff\xd8page-two\xff\xd9")
        server_module.THESIS_PAGES_ROOT = reader_root
        cls.server = CyclingServer(("127.0.0.1", 0), CyclingHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.reader_assets.cleanup()

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
        self.assertNotIn("<iframe", html)
        self.assertNotIn("Otwórz PDF", html)
        self.assertNotIn(">Pobierz<", html)

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

    def test_thesis_reader_serves_tokenized_page_images(self):
        _, manifest, headers = self.json_request("/api/thesis/manifest")
        self.assertEqual(manifest["pages"], 2)
        self.assertEqual(headers["Cache-Control"], "no-store")
        page_url = manifest["page_url"].replace("{page}", "1") + "?t=" + manifest["token"]
        with urlopen(self.base + page_url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers["Content-Type"], "image/jpeg")
            self.assertEqual(response.headers["Cache-Control"], "private, no-store, max-age=0")
            self.assertEqual(response.read(2), b"\xff\xd8")

        with self.assertRaises(HTTPError) as context:
            urlopen(self.base + "/thesis/pages/1.jpg?t=invalid", timeout=3)
        self.assertEqual(context.exception.code, 404)

    def test_original_pdf_paths_are_gone_even_with_queries(self):
        paths = (
            "/thesis/INF.MN-152863-6350.pdf",
            "/thesis/master-thesis-pl.pdf?download=1",
            "/static/master-thesis-pl.pdf?cache=old",
            "/another-copy.pdf?x=1",
        )
        for path in paths:
            with self.subTest(path=path), self.assertRaises(HTTPError) as context:
                urlopen(self.base + path, timeout=3)
            self.assertEqual(context.exception.code, 410)
            self.assertEqual(context.exception.headers["Cache-Control"], "no-store")

    def test_analysis_stats_match_known_data_math(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text(
            "y_true,y_pred\n"
            "100.0,110.0\n"
            "100.0,105.0\n"
            "100.0,90.0\n"
            "100.0,101.0\n"
            "120.0,125.0\n",
            encoding="utf-8",
        )
        (root / "baseline_predictions_variant_c.csv").write_text(
            "y_true,y_pred\n"
            "100.0,95.0\n"
            "100.0,107.0\n"
            "150.0,151.0\n",
            encoding="utf-8",
        )
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B")
            self.assertEqual(body["metadata"], {
                "variant": "Variant_B",
                "ftp_min": 0.0,
                "ftp_max": None,
                "model": "XGBoost",
                "scope": "baseline_prediction_files",
            })
            self.assertEqual(body["stats"], {
                "count": 5,
                "total_count": 5,
                "mae": 6.2,
                "rmse": 7.085,
                "median_ae": 5.0,
                "bias": 2.2,
                "within_5": 60.0,
                "within_10": 100.0,
                "within_20": 100.0,
            })
            self.assertEqual(
                body["points"],
                [
                    {"actual": 100.0, "predicted": 110.0},
                    {"actual": 100.0, "predicted": 105.0},
                    {"actual": 100.0, "predicted": 90.0},
                    {"actual": 100.0, "predicted": 101.0},
                    {"actual": 120.0, "predicted": 125.0},
                ],
            )

            _, body, _ = self.json_request("/api/analysis?variant=Variant_B&ftp_min=110&ftp_max=130")
            self.assertEqual(body["metadata"]["ftp_min"], 110.0)
            self.assertEqual(body["metadata"]["ftp_max"], 130.0)
            self.assertEqual(body["stats"]["count"], 1)
            self.assertEqual(body["stats"]["total_count"], 5)
            self.assertEqual(body["stats"]["mae"], 5.0)
            self.assertEqual(body["stats"]["rmse"], 5.0)
            self.assertEqual(body["stats"]["bias"], 5.0)
            self.assertEqual(body["points"], [{"actual": 120.0, "predicted": 125.0}])

            _, body, _ = self.json_request("/api/analysis?variant=Variant_C")
            self.assertEqual(body["stats"]["count"], 3)
            self.assertEqual(body["stats"]["mae"], 4.333)
            self.assertEqual(body["stats"]["rmse"], 5.0)
            self.assertEqual(body["stats"]["median_ae"], 5.0)
            self.assertEqual(body["stats"]["bias"], 1.0)
            self.assertEqual(body["stats"]["within_5"], 66.7)
            self.assertEqual(body["stats"]["within_10"], 100.0)

            _, body, _ = self.json_request("/api/analysis?variant=Variant_C&ftp_max=100")
            self.assertEqual(body["stats"]["count"], 2)
            self.assertEqual(
                body["points"],
                [{"actual": 100.0, "predicted": 95.0}, {"actual": 100.0, "predicted": 107.0}],
            )

            _, body, _ = self.json_request("/api/analysis?variant=Variant_C&ftp_max=150")
            self.assertEqual(body["stats"]["count"], 3)
            self.assertEqual(body["points"][2], {"actual": 150.0, "predicted": 151.0})
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_even_count_median_uses_average(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text(
            "y_true,y_pred\n"
            "100.0,105.0\n"
            "100.0,93.0\n",
            encoding="utf-8",
        )
        (root / "baseline_predictions_variant_c.csv").write_text("y_true,y_pred\n", encoding="utf-8")
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B")
            self.assertEqual(body["stats"]["median_ae"], 6.0)
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_reports_negative_bias(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text(
            "y_true,y_pred\n"
            "100.0,95.0\n"
            "100.0,92.0\n",
            encoding="utf-8",
        )
        (root / "baseline_predictions_variant_c.csv").write_text("y_true,y_pred\n", encoding="utf-8")
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B")
            self.assertEqual(body["stats"]["bias"], -6.5)
            self.assertEqual(body["stats"]["mae"], 6.5)
            self.assertEqual(body["stats"]["rmse"], 6.671)
            self.assertEqual(body["stats"]["median_ae"], 6.5)
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_empty_filter_keeps_top_level_counts(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text(
            "y_true,y_pred\n100.0,95.0\n",
            encoding="utf-8",
        )
        (root / "baseline_predictions_variant_c.csv").write_text("y_true,y_pred\n", encoding="utf-8")
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B&ftp_min=110")
            self.assertIsNone(body["stats"])
            self.assertEqual(body["count"], 0)
            self.assertEqual(body["total_count"], 1)
            self.assertEqual(body["points"], [])
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_sampling_includes_last_point(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text(
            "y_true,y_pred\n" + "".join(f"{i},{i + 1}\n" for i in range(150)),
            encoding="utf-8",
        )
        (root / "baseline_predictions_variant_c.csv").write_text("y_true,y_pred\n", encoding="utf-8")
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B")
            self.assertEqual(len(body["points"]), 120)
            self.assertEqual(body["points"][-1], {"actual": 149.0, "predicted": 150.0})
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_returns_at_most_120_points(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        for suffix in ("b", "c"):
            (root / f"baseline_predictions_variant_{suffix}.csv").write_text(
                "y_true,y_pred\n" + "".join(f"{i},{i + 1}\n" for i in range(150)),
                encoding="utf-8",
            )
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            for variant in ("Variant_B", "Variant_C"):
                _, body, _ = self.json_request(f"/api/analysis?variant={variant}")
                self.assertEqual(len(body["points"]), 120)
                self.assertEqual(body["stats"]["count"], 150)
                self.assertEqual(body["stats"]["total_count"], 150)
                self.assertEqual(body["points"][0], {"actual": 0.0, "predicted": 1.0})
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_stats_are_null_for_empty_results(self):
        assets = tempfile.TemporaryDirectory()
        root = Path(assets.name)
        (root / "baseline_predictions_variant_b.csv").write_text("y_true,y_pred\n", encoding="utf-8")
        (root / "baseline_predictions_variant_c.csv").write_text("y_true,y_pred\n1.0,2.0\n", encoding="utf-8")
        old_root = server_module.RESULTS_ROOT
        server_module.RESULTS_ROOT = root
        try:
            _, body, _ = self.json_request("/api/analysis?variant=Variant_B")
            self.assertIsNone(body["stats"])
            self.assertEqual(body["points"], [])
            _, body, _ = self.json_request("/api/analysis?variant=Variant_C&ftp_min=10&ftp_max=20")
            self.assertIsNone(body["stats"])
            self.assertEqual(body["points"], [])
        finally:
            server_module.RESULTS_ROOT = old_root
            assets.cleanup()

    def test_analysis_rejects_invalid_inputs(self):
        queries = (
            "/api/analysis?variant=Variant_A",
            "/api/analysis?variant=Variant_B&ftp_min=abc",
            "/api/analysis?variant=Variant_B&ftp_min=-5",
            "/api/analysis?variant=Variant_B&ftp_max=nan",
            "/api/analysis?variant=Variant_B&ftp_min=100&ftp_max=50",
        )
        for path in queries:
            with self.subTest(path=path), self.assertRaises(HTTPError) as context:
                self.json_request(path)
            self.assertEqual(context.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
