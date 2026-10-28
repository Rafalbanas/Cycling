"""Unit tests for the root-owned deployment receiver; restart and healthy are replaced with stubs."""
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zipfile import ZipFile, ZipInfo

import receive as receive_module


REV = "0123456789abcdef0123456789abcdef01234567"
OLD_REV = "fedcba9876543210fedcba9876543210fedcba9876"

RELEASE_FILES = {
    "webapp/server.py": "def main():\n    print('ok')\n",
    "webapp/index.html": "<html><body>ok</body></html>",
    "webapp/static/app.js": "const x = 1;\n",
    "webapp/static/styles.css": "body { margin: 0; }\n",
    "webapp/static/favicon.svg": "<svg></svg>",
    "results/model_comparison_partial.csv": "Variant,Model\nB,XGBoost\n",
    "results/error_by_ftp_bins.csv": "FTP range,Samples\nA,1\n",
    "results/shap_importance_variant_b.csv": "Feature,Mean_Abs_SHAP\na,0.1\n",
    "results/shap_importance_variant_c.csv": "Feature,Mean_Abs_SHAP\na,0.1\n",
    "results/baseline_predictions_variant_b.csv": "y_true,y_pred\n",
    "results/baseline_predictions_variant_c.csv": "y_true,y_pred\n",
    "experiments/control_5000/results/control_5000_data_stats.json": "{\"athletes_after_ftp_filter\": 1}",
    "experiments/control_5000/results/control_5000_metrics.csv": "Variant,Model\nB,XGBoost\n",
}


def build_archive(revision=REV, extra=()):
    buffer = io.BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr("revision.txt", revision + "\n")
        for name, content in RELEASE_FILES.items():
            archive.writestr(name, content)
        for name, content in extra:
            archive.writestr(name, content)
    return buffer.getvalue()


class FakeResponse:
    """Bounded standalone response for urlopen; read(n) is capped like urlopen's."""

    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return None

    def read(self, size):
        return self.body[:size]


class ReceiverTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.state = Path(self.root.name) / "state"
        self.state.mkdir(parents=True)
        self.legacy = Path(self.root.name) / "legacy"
        self.legacy.mkdir()
        self.config = {
            "state_dir": str(self.state),
            "health_url": "http://127.0.0.1:1",
            "health_attempts": 1,
            "health_interval": 0,
        }

    def tearDown(self):
        self.root.cleanup()

    def run_deploy(self, payload, revision, healthy_value=True, digest=None):
        self.restarts = []
        if digest is None:
            digest = hashlib.sha256(payload).hexdigest()

        def restart(_config):
            self.restarts.append(1)

        with mock.patch.object(receive_module, "restart", restart), \
              mock.patch.object(receive_module, "healthy", lambda *args, **kwargs: healthy_value), \
              mock.patch.object(receive_module, "LEGACY", self.legacy):
            receive_module.deploy(self.config, revision, digest, io.BytesIO(payload))

    def fake_urlopen(self, health_body, analysis_body, calls=None):
        def urlopen(url, timeout=3):
            body = health_body if url.endswith("/healthz") else analysis_body
            if calls is not None:
                calls.append(url)
            return FakeResponse(body)

        return urlopen

    def run_deploy_real_healthy(self, payload, revision, health_body, analysis_body, calls=None):
        """Runs the real deploy flow; only restart/LEGACY are stubbed, healthy is not."""
        self.restarts = []

        def restart(_config):
            self.restarts.append(1)

        with mock.patch.object(receive_module, "restart", restart), \
              mock.patch.object(receive_module, "urlopen", self.fake_urlopen(health_body, analysis_body, calls)), \
              mock.patch.object(receive_module, "LEGACY", self.legacy):
            receive_module.deploy(self.config, revision, hashlib.sha256(payload).hexdigest(), io.BytesIO(payload))

    def test_status_is_uninitialized_before_first_deploy(self):
        self.assertEqual(receive_module.status(self.state), "uninitialized")

    def test_status_reports_legacy_directory_without_revision(self):
        (self.state / "current").symlink_to(self.legacy)
        self.assertEqual(receive_module.status(self.state), "uninitialized")

    def test_first_deploy_success_updates_current_and_status(self):
        payload = build_archive()
        self.run_deploy(payload, REV)
        current = self.state / "current"
        release = current.resolve(strict=True)
        digest = hashlib.sha256(payload).hexdigest()
        self.assertEqual(release, self.state / "releases" / (REV + "-" + digest[:16]))
        self.assertEqual(receive_module.status(self.state), REV)
        self.assertEqual(self.restarts, [1])
        previous = (self.state / "previous").read_text().strip()
        self.assertEqual(previous, str(self.legacy))
        for directory in sorted(release.rglob("*")):
            if directory.is_dir():
                self.assertEqual(stat.S_IMODE(os.stat(directory).st_mode), 0o755)
        for entry in sorted(RELEASE_FILES) + ["revision.txt"]:
            self.assertEqual(stat.S_IMODE(os.stat(release / entry).st_mode), 0o644)

    def test_failed_deploy_rolls_back_to_previous_release(self):
        old = self.state / "releases" / (OLD_REV + "0123456789abcdef")
        old.mkdir(parents=True)
        (old / "revision.txt").write_text(OLD_REV + "\n")
        (self.state / "current").symlink_to(old)
        with self.assertRaises(RuntimeError):
            self.run_deploy(build_archive(), REV, healthy_value=False)
        self.assertEqual((self.state / "current").resolve(strict=True), old)
        self.assertEqual(receive_module.status(self.state), OLD_REV)
        self.assertEqual(self.restarts, [1, 1])

    def test_failed_first_deploy_rolls_back_to_legacy(self):
        with self.assertRaises(RuntimeError):
            self.run_deploy(build_archive(), REV, healthy_value=False)
        self.assertEqual((self.state / "current").resolve(strict=True), self.legacy)
        self.assertEqual(receive_module.status(self.state), "uninitialized")
        self.assertEqual(self.restarts, [1, 1])

    def test_rejects_digest_mismatch(self):
        payload = build_archive()
        with mock.patch.object(receive_module, "restart", None), \
              mock.patch.object(receive_module, "healthy", lambda *args, **kwargs: True), \
              mock.patch.object(receive_module, "LEGACY", self.legacy):
            with self.assertRaises(ValueError):
                receive_module.deploy(
                    self.config, REV, "0" * 64, io.BytesIO(payload)
                )

    def test_rejects_archive_larger_than_compressed_limit(self):
        payload = b"x" * (receive_module.MAX_BYTES + 1)
        with self.assertRaises(ValueError):
            self.run_deploy(payload, REV)

    def test_rejects_archive_larger_than_expanded_limit(self):
        # One release entry exceeds the expanded bound; the compressed size stays small.
        # The real digest is used, so only the size check can fail.
        payload = io.BytesIO()
        with ZipFile(payload, "w") as zip_:
            zip_.writestr("revision.txt", REV + "\n")
            for name, content in RELEASE_FILES.items():
                if name != "webapp/server.py":
                    zip_.writestr(name, content)
            zip_.writestr("webapp/server.py", "x" * (receive_module.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            self.run_deploy(payload.getbuffer(), REV)

    def test_rejects_unexpected_entries(self):
        with self.assertRaises(ValueError):
            self.run_deploy(
                build_archive(extra=[("webapp/extra.html", "<html></html>")]), REV
            )

    def test_real_health_accepts_matching_revision_and_analysis(self):
        self.run_deploy_real_healthy(
            build_archive(), REV,
            json.dumps({"status": "ok", "revision": REV}).encode(),
            b'{"count": 1}',
        )
        self.assertEqual(receive_module.status(self.state), REV)

    def test_real_health_rejects_wrong_revision_and_rolls_back(self):
        with self.assertRaises(RuntimeError):
            self.run_deploy_real_healthy(
                build_archive(), REV,
                json.dumps({"status": "ok", "revision": OLD_REV}).encode(),
                b'{"count": 1}',
            )
        self.assertEqual((self.state / "current").resolve(), self.legacy)

    def test_rejects_symlink_entry(self):
        buffer = io.BytesIO()
        with ZipFile(buffer, "w") as archive:
            archive.writestr("revision.txt", REV + "\n")
            for name, content in RELEASE_FILES.items():
                if name == "webapp/server.py":
                    entry = ZipInfo(name)
                    entry.create_system = 3
                    entry.external_attr = (stat.S_IFLNK | 0o777) << 16
                    archive.writestr(entry, "/etc/passwd")
                else:
                    archive.writestr(name, content)
        with self.assertRaises(ValueError):
            self.run_deploy(buffer.getvalue(), REV)

    def test_rejects_duplicate_entries(self):
        payload = io.BytesIO()
        with ZipFile(payload, "w") as archive:
            archive.writestr("revision.txt", REV + "\n")
            for name, content in RELEASE_FILES.items():
                if name != "webapp/index.html":
                    archive.writestr(name, content)
            archive.writestr("webapp/index.html", "duplicate")
            archive.writestr("webapp/index.html", "duplicate")
        with self.assertRaises(ValueError):
            self.run_deploy(payload.getbuffer(), REV)

    def test_rejects_directory_entries(self):
        payload = io.BytesIO()
        with ZipFile(payload, "w") as archive:
            archive.writestr("revision.txt", REV + "\n")
            for name, content in RELEASE_FILES.items():
                if name != "webapp/server.py":
                    archive.writestr(name, content)
            archive.writestr("webapp/server.py", "def main():\n    print('ok')\n")
            archive.writestr("webapp/static/", "")
        with self.assertRaises(ValueError):
            self.run_deploy(payload.getbuffer(), REV)

    def test_rejects_revision_mismatch_inside_archive(self):
        with self.assertRaises(ValueError):
            self.run_deploy(build_archive(revision=OLD_REV), REV)

    def test_rejects_invalid_shapes(self):
        payload = build_archive()
        digest = hashlib.sha256(payload).hexdigest()
        with mock.patch.object(receive_module, "restart", None), \
              mock.patch.object(receive_module, "healthy", lambda *args, **kwargs: True), \
              mock.patch.object(receive_module, "LEGACY", self.legacy):
            with self.assertRaises(ValueError):
                receive_module.deploy(
                    self.config, "0" * 39, digest, io.BytesIO(payload)
                )
            with self.assertRaises(ValueError):
                receive_module.deploy(self.config, REV, "0" * 65, io.BytesIO(payload))

    def test_rejects_broken_server_syntax(self):
        payload = io.BytesIO()
        with ZipFile(payload, "w") as archive:
            archive.writestr("revision.txt", REV + "\n")
            for name, content in RELEASE_FILES.items():
                if name != "webapp/server.py":
                    archive.writestr(name, content)
            archive.writestr("webapp/server.py", "def broken(  # syntax error")
        with self.assertRaises(SyntaxError):
            self.run_deploy(payload.getbuffer(), REV)

    def test_main_dispatch_rejects_unknown_commands(self):
        config_path = self.state / "deploy.json"
        config_path.write_text(
            json.dumps({"state_dir": str(self.state), "health_url": "http://127.0.0.1:1"})
        )
        with mock.patch.object(receive_module, "CONFIG", config_path), \
             mock.patch.object(sys, "argv", ["receive.py"]):
            with self.assertRaises(SystemExit) as context:
                receive_module.main()
        with mock.patch.object(receive_module, "CONFIG", config_path), \
             mock.patch.object(sys, "argv", ["receive.py", "deploy", "x"] * 2):
            with self.assertRaises(SystemExit) as context:
                receive_module.main()
        self.assertEqual(context.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
