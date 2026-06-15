#!/bin/bash
# =============================================================================
# Hetzner Server Provisioning & Initial Setup Script
# Run once on a fresh Hetzner Ubuntu 22.04 server
# Usage: bash hetzner_setup.sh
# =============================================================================
set -euo pipefail

DEPLOY_DIR="/opt/smartrecipe"
DOCKER_COMPOSE_VERSION="2.27.0"
APP_USER="deploy"

echo "==> [1/7] Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq

echo "==> [2/7] Installing dependencies..."
apt-get install -y -qq \
  curl \
  git \
  ufw \
  fail2ban \
  ca-certificates \
  gnupg \
  lsb-release

echo "==> [3/7] Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin

systemctl enable docker
systemctl start docker

echo "==> [4/7] Installing Docker Compose..."
curl -fsSL \
  "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "==> [5/7] Creating deploy user..."
if ! id "${APP_USER}" &>/dev/null; then
  useradd -m -s /bin/bash "${APP_USER}"
  usermod -aG docker "${APP_USER}"
fi

echo "==> [6/7] Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp   # Grafana
ufw allow 9090/tcp   # Prometheus
ufw status

echo "==> [7/7] Creating app directory..."
mkdir -p "${DEPLOY_DIR}"
chown "${APP_USER}:${APP_USER}" "${DEPLOY_DIR}"
mkdir -p /opt/smartrecipe/{mysql_data,prometheus_data,grafana_data}
chown -R "${APP_USER}:${APP_USER}" /opt/smartrecipe

echo ""
echo "========================================================"
echo "Hetzner server setup complete!"
echo "Next steps:"
echo "  1. Copy .env file to ${DEPLOY_DIR}/.env"
echo "  2. Copy docker-compose.yml and docker-compose.prod.yml"
echo "  3. Run: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d"
echo "========================================================"
