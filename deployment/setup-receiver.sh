#!/usr/bin/env bash
# Run as root once before registering the dedicated production runner.
set -euo pipefail
project=$(cd -- "$(dirname -- "$0")/.." && pwd)
runner_user=cycling-runner
if ! id "$runner_user" >/dev/null 2>&1; then
    useradd --system --create-home --home-dir /var/lib/cycling-runner --shell /bin/bash "$runner_user"
fi
install -d -o root -g root -m 0755 /etc/cycling-web /var/lib/cycling-deploy
install -o root -g root -m 0755 "$project/deployment/receive.py" /usr/local/sbin/cycling-deploy
install -o root -g root -m 0755 "$project/deployment/runner-guard.sh" /usr/local/sbin/cycling-runner-guard.sh
if [[ ! -e /etc/cycling-web/deploy.json ]]; then
    cat > /etc/cycling-web/deploy.json <<'EOF'
{"state_dir":"/var/lib/cycling-deploy","health_url":"http://127.0.0.1:20144","health_attempts":10,"health_interval":2}
EOF
    chmod 0644 /etc/cycling-web/deploy.json
fi
if [[ ! -e /var/lib/cycling-deploy/current ]]; then
    ln -s /opt/cycling-web /var/lib/cycling-deploy/current
fi
cat > /etc/sudoers.d/cycling-deploy <<'EOF'
cycling-runner ALL=(root) NOPASSWD: /usr/local/sbin/cycling-deploy
EOF
chmod 0440 /etc/sudoers.d/cycling-deploy
visudo -cf /etc/sudoers.d/cycling-deploy
install -d -m 0755 /etc/systemd/system/cycling-web.service.d
cat > /etc/systemd/system/cycling-web.service.d/releases.conf <<'EOF'
[Service]
WorkingDirectory=/var/lib/cycling-deploy/current
ExecStart=
ExecStart=/usr/bin/python3 /var/lib/cycling-deploy/current/webapp/server.py
ReadOnlyPaths=/var/lib/cycling-deploy
EOF
systemctl daemon-reload
echo 'Receiver ready; the next deployment will switch the running service.'
