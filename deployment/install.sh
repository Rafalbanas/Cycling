#!/bin/sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DEPLOY_ROOT=/opt/cycling-web
SERVICE_USER=cycling-web

if ! id "$SERVICE_USER" >/dev/null 2>&1; then
    useradd --system --home-dir /nonexistent --shell /usr/sbin/nologin "$SERVICE_USER"
fi

install -d -o root -g "$SERVICE_USER" -m 0750 \
    "$DEPLOY_ROOT/webapp/static" \
    "$DEPLOY_ROOT/results" \
    "$DEPLOY_ROOT/experiments/control_5000/results"

install -o root -g "$SERVICE_USER" -m 0640 \
    "$PROJECT_ROOT/webapp/server.py" \
    "$PROJECT_ROOT/webapp/index.html" \
    "$DEPLOY_ROOT/webapp/"
install -o root -g "$SERVICE_USER" -m 0640 \
    "$PROJECT_ROOT/webapp/static/styles.css" \
    "$PROJECT_ROOT/webapp/static/app.js" \
    "$PROJECT_ROOT/webapp/static/favicon.svg" \
    "$PROJECT_ROOT/webapp/static/master-thesis-pl.pdf" \
    "$DEPLOY_ROOT/webapp/static/"

install -o root -g "$SERVICE_USER" -m 0640 \
    "$PROJECT_ROOT/results/model_comparison_partial.csv" \
    "$PROJECT_ROOT/results/error_by_ftp_bins.csv" \
    "$PROJECT_ROOT/results/shap_importance_variant_b.csv" \
    "$PROJECT_ROOT/results/shap_importance_variant_c.csv" \
    "$PROJECT_ROOT/results/baseline_predictions_variant_b.csv" \
    "$PROJECT_ROOT/results/baseline_predictions_variant_c.csv" \
    "$DEPLOY_ROOT/results/"
install -o root -g "$SERVICE_USER" -m 0640 \
    "$PROJECT_ROOT/experiments/control_5000/results/control_5000_data_stats.json" \
    "$PROJECT_ROOT/experiments/control_5000/results/control_5000_metrics.csv" \
    "$DEPLOY_ROOT/experiments/control_5000/results/"

install -o root -g root -m 0644 "$PROJECT_ROOT/deployment/cycling-web.service" /etc/systemd/system/cycling-web.service
install -o root -g root -m 0644 "$PROJECT_ROOT/deployment/nginx-cycling.conf" /etc/nginx/sites-available/cycling.conf
if [ ! -e /etc/nginx/sites-enabled/cycling.conf ]; then
    ln -s /etc/nginx/sites-available/cycling.conf /etc/nginx/sites-enabled/cycling.conf
fi

systemctl daemon-reload
systemctl enable --now cycling-web.service
systemctl restart cycling-web.service
attempt=0
until curl --fail --silent http://127.0.0.1:20144/healthz >/dev/null; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 20 ]; then
        echo "cycling-web.service nie osiągnęła gotowości" >&2
        exit 1
    fi
    sleep 1
done
nginx -t
systemctl reload nginx
