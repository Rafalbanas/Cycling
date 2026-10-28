#!/usr/bin/env python3
"""Dependency-free HTTP application presenting the thesis' verified results."""

from __future__ import annotations

import csv
import json
import math
import logging
import os
import re
import secrets
import statistics
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = WEB_ROOT / "static"
RESULTS_ROOT = ROOT / "results"
CONTROL_ROOT = ROOT / "experiments" / "control_5000" / "results"
THESIS_PAGES_ROOT = Path(os.environ.get("CYCLING_THESIS_PAGES", "/var/lib/cycling-web/thesis-pages"))
THESIS_ACCESS_TOKEN = secrets.token_urlsafe(24)

HOST = os.environ.get("CYCLING_HOST", "127.0.0.1")
PORT = int(os.environ.get("CYCLING_PORT", "20144"))

def read_revision() -> str:
    path = ROOT / "revision.txt"
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"

REVISION = read_revision()

STATIC_FILES = {
    "/": (WEB_ROOT / "index.html", "text/html; charset=utf-8"),
    "/index.html": (WEB_ROOT / "index.html", "text/html; charset=utf-8"),
    "/static/styles.css": (STATIC_ROOT / "styles.css", "text/css; charset=utf-8"),
    "/static/app.js": (STATIC_ROOT / "app.js", "text/javascript; charset=utf-8"),
    "/static/favicon.svg": (STATIC_ROOT / "favicon.svg", "image/svg+xml"),
}

VARIANT_LABELS = {
    "Variant_A": "A · z MMP20 (wyciek)",
    "Variant_B": "B · bez MMP20",
    "Variant_C": "C · bez cech MMP",
}

DATASET = {
    "sessions": 151_399,
    "athletes": 726,
    "archives": 781,
    "label": "0,95 × najlepsza średnia moc z 20 min",
    "split": "osobniczy, GroupShuffleSplit 80/20",
}

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        "connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; "
        "form-action 'self'"
    ),
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}

MESSAGES = {
    "pl": {
        "missing_resource": "Nie znaleziono zasobu.",
        "variants": "Dostępne warianty: Variant_B lub Variant_C.",
        "integer_limit": "Parametr limit musi być liczbą całkowitą.",
        "limit_range": "Parametr limit musi mieścić się w zakresie 10–300.",
        "missing_page": "Nie znaleziono strony.",
        "missing_endpoint": "Nie znaleziono endpointu.",
        "content_type": "Wymagany Content-Type: application/json.",
        "content_length": "Nieprawidłowy Content-Length.",
        "body_size": "Treść żądania musi mieć od 1 B do 16 KiB.",
        "invalid_power": "Podaj prawidłową wartość mocy z 20 minut.",
        "power_range": "Moc 20-minutowa musi mieścić się w zakresie 50–800 W.",
        "weight_range": "Masa ciała musi mieścić się w zakresie 30–250 kg.",
        "range": "Nieprawidłowy zakres bajtów.",
        "ftp_bound_number": "Parametry ftp_min/ftp_max muszą być liczbami.",
        "ftp_bound_range": "Parametry ftp_min/ftp_max muszą być nieujemne i spełniać ftp_min <= ftp_max.",
        "document_unavailable": "Oryginalny dokument PDF nie jest udostępniany publicznie.",
        "reader_unavailable": "Czytnik pracy jest tymczasowo niedostępny.",
        "kind": "operacyjna etykieta FTP",
        "notice": "Wynik heurystyczny; nie zastępuje testu fizjologicznego ani porady trenera.",
    },
    "en": {
        "missing_resource": "Resource not found.",
        "variants": "Available variants: Variant_B or Variant_C.",
        "integer_limit": "The limit parameter must be an integer.",
        "limit_range": "The limit parameter must be between 10 and 300.",
        "missing_page": "Page not found.",
        "missing_endpoint": "Endpoint not found.",
        "content_type": "Content-Type: application/json is required.",
        "content_length": "Invalid Content-Length.",
        "body_size": "The request body must be between 1 B and 16 KiB.",
        "invalid_power": "Enter a valid 20-minute power value.",
        "power_range": "20-minute power must be between 50 and 800 W.",
        "weight_range": "Body mass must be between 30 and 250 kg.",
        "range": "Invalid byte range.",
        "ftp_bound_number": "The ftp_min and ftp_max parameters must be numbers.",
        "ftp_bound_range": "The ftp_min and ftp_max parameters must be non-negative with ftp_min <= ftp_max.",
        "document_unavailable": "The original PDF document is not publicly available.",
        "reader_unavailable": "The thesis reader is temporarily unavailable.",
        "kind": "operational FTP label",
        "notice": "This is a heuristic result; it does not replace physiological testing or coaching advice.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def model_results() -> list[dict[str, object]]:
    rows = read_csv(RESULTS_ROOT / "model_comparison_partial.csv")
    output: list[dict[str, object]] = []
    for row in rows:
        output.append(
            {
                "variant": row["Variant"],
                "variant_label": VARIANT_LABELS[row["Variant"]],
                "model": row["Model"],
                "mae": round(float(row["MAE"]), 3),
                "rmse": round(float(row["RMSE"]), 3),
                "r2": round(float(row["R2"]), 4),
                "median_ae": round(float(row["MedAE"]), 3),
                "test_records": int(row["Test_Records"]),
                "leakage": row["Variant"] == "Variant_A",
            }
        )
    return output


def error_ranges() -> list[dict[str, object]]:
    rows = read_csv(RESULTS_ROOT / "error_by_ftp_bins.csv")
    return [
        {
            "range": row["FTP range"],
            "samples": int(row["Samples"]),
            "athletes": int(row["Athletes"]),
            "mae": float(row["MAE [W]"]),
            "mape": float(row["MAPE [%]"]),
        }
        for row in rows
    ]


def feature_importance(variant: str) -> list[dict[str, object]]:
    suffix = "B" if variant == "Variant_B" else "C"
    rows = read_csv(RESULTS_ROOT / f"shap_importance_variant_{suffix.lower()}.csv")
    return [
        {"feature": row["Feature"], "importance": round(float(row["Mean_Abs_SHAP"]), 4)}
        for row in rows[:10]
    ]


def supplemental_control() -> dict[str, object]:
    stats = json.loads((CONTROL_ROOT / "control_5000_data_stats.json").read_text(encoding="utf-8"))
    rows = read_csv(CONTROL_ROOT / "control_5000_metrics.csv")
    best_b = min((row for row in rows if row["Variant"] == "Variant_B"), key=lambda row: float(row["MAE"]))
    best_c = min((row for row in rows if row["Variant"] == "Variant_C"), key=lambda row: float(row["MAE"]))
    return {
        "athletes": stats["athletes_after_ftp_filter"],
        "sessions": stats["sessions_after_ftp_filter"],
        "scope": {
            "pl": "uzupełniająca kontrola skalowalności, nie wynik główny pracy",
            "en": "supplementary scalability check, not the thesis's main result",
        },
        "variant_b": {"model": best_b["Model"], "mae": round(float(best_b["MAE"]), 2)},
        "variant_c": {"model": best_c["Model"], "mae": round(float(best_c["MAE"]), 2)},
    }


def prediction_points(variant: str, limit: int) -> list[dict[str, float]]:
    suffix = "b" if variant == "Variant_B" else "c"
    rows = read_csv(RESULTS_ROOT / f"baseline_predictions_variant_{suffix}.csv")
    if not rows:
        return []
    stride = max(1, len(rows) // limit)
    selected = rows[::stride][:limit]
    return [
        {
            "actual": round(float(row["y_true"]), 2),
            "predicted": round(float(row["y_pred"]), 2),
        }
        for row in selected
    ]


def analysis(variant: str, ftp_min: float, ftp_max: float | None) -> dict[str, object]:
    suffix = "b" if variant == "Variant_B" else "c"
    rows = read_csv(RESULTS_ROOT / f"baseline_predictions_variant_{suffix}.csv")
    values: list[tuple[float, float]] = []
    for row in rows:
        try:
            actual, predicted = float(row["y_true"]), float(row["y_pred"])
        except (KeyError, TypeError, ValueError):
            continue
        if not math.isfinite(actual) or not math.isfinite(predicted):
            continue
        if ftp_min <= actual and (ftp_max is None or actual <= ftp_max):
            values.append((actual, predicted))
    total = len(values)
    if total > 120:
        selected = [values[i * (total - 1) // (120 - 1)] for i in range(120)]
    else:
        selected = values
    points = [
        {"actual": round(actual, 2), "predicted": round(predicted, 2)}
        for actual, predicted in selected
    ]
    metadata = {
        "variant": variant,
        "ftp_min": ftp_min,
        "ftp_max": ftp_max,
        "model": "XGBoost",
        "scope": "baseline_prediction_files",
    }
    if not values:
        return {
            "metadata": metadata,
            "stats": None,
            "count": 0,
            "total_count": len(rows),
            "points": points,
        }
    residuals = [predicted - actual for actual, predicted in values]
    absolute = [abs(error) for error in residuals]
    return {
        "metadata": metadata,
        "stats": {
            "count": total,
            "total_count": len(rows),
            "mae": round(sum(absolute) / total, 3),
            "rmse": round(math.sqrt(sum(error * error for error in residuals) / total), 3),
            "median_ae": round(statistics.median(absolute), 3),
            "bias": round(sum(residuals) / total, 3),
            "within_5": round(100.0 * sum(count <= 5.0 for count in absolute) / total, 1),
            "within_10": round(100.0 * sum(count <= 10.0 for count in absolute) / total, 1),
            "within_20": round(100.0 * sum(count <= 20.0 for count in absolute) / total, 1),
        },
        "count": total,
        "total_count": len(rows),
        "points": points,
    }


SUMMARY = {
    "dataset": DATASET,
    "models": model_results(),
    "error_ranges": error_ranges(),
    "features": {
        "Variant_B": feature_importance("Variant_B"),
        "Variant_C": feature_importance("Variant_C"),
    },
    "supplemental_control": supplemental_control(),
    "methodology": {
        "source": "GoldenCheetah OpenData",
        "target": {"pl": "operacyjna, heurystyczna etykieta FTP", "en": "operational, heuristic FTP label"},
        "best_variant_b": "XGBoost · MAE 6,55 W · R² 0,9630",
        "best_variant_c": "XGBoost · MAE 10,29 W · R² 0,9170",
        "saved_model_available": False,
    },
}


class CyclingHandler(BaseHTTPRequestHandler):
    server_version = "CyclingWeb/1.0"
    sys_version = ""

    def log_message(self, fmt: str, *args: object) -> None:
        logging.info("%s %s", self.address_string(), fmt % args)

    def _headers(
        self,
        status: HTTPStatus,
        content_type: str,
        length: int,
        extra_headers: dict[str, str] | None = None,
        cache_control: str | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        default_cache = "no-store" if content_type.startswith("application/json") else "public, max-age=300"
        self.send_header("Cache-Control", cache_control or default_cache)
        for key, value in SECURITY_HEADERS.items():
            self.send_header(key, value)
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()

    def send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
        extra_headers: dict[str, str] | None = None,
        cache_control: str | None = None,
    ) -> None:
        self._headers(status, content_type, len(body), extra_headers, cache_control)
        if self.command != "HEAD":
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                logging.info("Client closed the response before transfer completed")

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_bytes(body, "application/json; charset=utf-8", status)

    def language(self, payload: dict | None = None) -> str:
        requested = str((payload or {}).get("lang", "")).lower()
        if requested in {"pl", "en"}:
            return requested
        return "en" if self.headers.get("Accept-Language", "").lower().startswith("en") else "pl"

    def send_error_json(self, status: HTTPStatus, message_key: str, language: str | None = None) -> None:
        lang = language or self.language()
        self.send_json({"error": MESSAGES[lang][message_key], "status": status.value}, status)

    @staticmethod
    def thesis_pages() -> list[Path]:
        def page_number(path: Path) -> int:
            match = re.search(r"(\d+)$", path.stem)
            return int(match.group(1)) if match else 0

        return sorted(THESIS_PAGES_ROOT.glob("page-*.jpg"), key=page_number)

    def send_thesis_page(self, parsed) -> None:
        token = parse_qs(parsed.query).get("t", [""])[0]
        if not secrets.compare_digest(token, THESIS_ACCESS_TOKEN):
            self.send_error_json(HTTPStatus.NOT_FOUND, "missing_resource")
            return
        match = re.fullmatch(r"/thesis/pages/(\d{1,3})\.jpg", parsed.path)
        pages = self.thesis_pages()
        page_number = int(match.group(1)) if match else 0
        if not 1 <= page_number <= len(pages):
            self.send_error_json(HTTPStatus.NOT_FOUND, "missing_resource")
            return
        try:
            body = pages[page_number - 1].read_bytes()
        except OSError:
            self.send_error_json(HTTPStatus.SERVICE_UNAVAILABLE, "reader_unavailable")
            return
        self.send_bytes(
            body,
            "image/jpeg",
            extra_headers={
                "Content-Disposition": f'inline; filename="thesis-page-{page_number}.jpg"',
                "X-Robots-Tag": "noindex, noarchive, noimageindex",
            },
            cache_control="private, no-store, max-age=0",
        )

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in STATIC_FILES:
            path, content_type = STATIC_FILES[parsed.path]
            try:
                self.send_bytes(path.read_bytes(), content_type)
            except FileNotFoundError:
                self.send_error_json(HTTPStatus.NOT_FOUND, "missing_resource")
            return
        if parsed.path.lower().endswith(".pdf"):
            self.send_error_json(HTTPStatus.GONE, "document_unavailable")
            return
        if parsed.path == "/healthz":
            self.send_json({"status": "ok", "service": "cycling-web", "revision": REVISION})
            return
        if parsed.path == "/api/summary":
            self.send_json(SUMMARY)
            return
        if parsed.path == "/api/thesis/manifest":
            page_count = len(self.thesis_pages())
            if not page_count:
                self.send_error_json(HTTPStatus.SERVICE_UNAVAILABLE, "reader_unavailable")
                return
            self.send_json(
                {
                    "pages": page_count,
                    "page_url": "/thesis/pages/{page}.jpg",
                    "token": THESIS_ACCESS_TOKEN,
                }
            )
            return
        if parsed.path.startswith("/thesis/pages/"):
            self.send_thesis_page(parsed)
            return
        if parsed.path == "/api/predictions":
            query = parse_qs(parsed.query)
            variant = query.get("variant", ["Variant_B"])[0]
            if variant not in {"Variant_B", "Variant_C"}:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "variants")
                return
            try:
                limit = int(query.get("limit", ["120"])[0])
            except ValueError:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "integer_limit")
                return
            if not 10 <= limit <= 300:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "limit_range")
                return
            self.send_json({"variant": variant, "points": prediction_points(variant, limit)})
            return
        if parsed.path == "/api/analysis":
            query = parse_qs(parsed.query)
            variant = query.get("variant", ["Variant_B"])[0]
            if variant not in {"Variant_B", "Variant_C"}:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "variants")
                return
            bounds: dict[str, float] = {}
            for name in ("ftp_min", "ftp_max"):
                if name not in query:
                    continue
                try:
                    bounds[name] = float(query[name][0])
                except ValueError:
                    self.send_error_json(HTTPStatus.BAD_REQUEST, "ftp_bound_number")
                    return
                if not math.isfinite(bounds[name]) or bounds[name] < 0:
                    self.send_error_json(HTTPStatus.BAD_REQUEST, "ftp_bound_range")
                    return
            if "ftp_min" in bounds and "ftp_max" in bounds and bounds["ftp_min"] > bounds["ftp_max"]:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "ftp_bound_range")
                return
            self.send_json(
                analysis(variant, bounds.get("ftp_min", 0.0), bounds.get("ftp_max"))
            )
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "missing_page")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/estimate":
            self.send_error_json(HTTPStatus.NOT_FOUND, "missing_endpoint")
            return
        if self.headers.get_content_type() != "application/json":
            self.send_error_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "content_type")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "content_length")
            return
        if length <= 0 or length > 16_384:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "body_size")
            return
        payload = None
        try:
            payload = json.loads(self.rfile.read(length))
            mmp20 = float(payload["mmp20"])
            weight_raw = payload.get("weight")
            weight = float(weight_raw) if weight_raw not in (None, "") else None
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self.send_error_json(HTTPStatus.BAD_REQUEST, "invalid_power", self.language(payload))
            return
        lang = self.language(payload)
        if not 50 <= mmp20 <= 800:
            self.send_error_json(HTTPStatus.UNPROCESSABLE_ENTITY, "power_range", lang)
            return
        if weight is not None and not 30 <= weight <= 250:
            self.send_error_json(HTTPStatus.UNPROCESSABLE_ENTITY, "weight_range", lang)
            return

        ftp = round(mmp20 * 0.95, 1)
        response = {
            "mmp20": round(mmp20, 1),
            "ftp": ftp,
            "watts_per_kg": round(ftp / weight, 2) if weight else None,
            "method": "0,95 × MMP20",
            "kind": MESSAGES[lang]["kind"],
            "notice": MESSAGES[lang]["notice"],
        }
        self.send_json(response)


class CyclingServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not re.fullmatch(r"\d{1,5}", str(PORT)) or not 1 <= PORT <= 65535:
        raise SystemExit("CYCLING_PORT musi być prawidłowym numerem portu.")
    server = CyclingServer((HOST, PORT), CyclingHandler)
    logging.info("Cycling Web listening on http://%s:%s", HOST, PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
