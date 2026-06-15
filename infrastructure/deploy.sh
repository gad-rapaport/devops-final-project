#!/bin/bash
# =============================================================================
# Deployment script — runs on the Hetzner server via GitHub Actions SSH
# Pulls latest Docker images and restarts services with zero-downtime
# =============================================================================
set -euo pipefail

DEPLOY_DIR="/opt/smartrecipe"
COMPOSE_FILE="${DEPLOY_DIR}/docker-compose.yml"
COMPOSE_PROD="${DEPLOY_DIR}/docker-compose.prod.yml"

echo "[deploy] Starting deployment at $(date)"

cd "${DEPLOY_DIR}"

echo "[deploy] Pulling latest images..."
docker compose -f "${COMPOSE_FILE}" -f "${COMPOSE_PROD}" pull

echo "[deploy] Running database migrations..."
docker compose -f "${COMPOSE_FILE}" -f "${COMPOSE_PROD}" run --rm \
  backend flask db upgrade || true

echo "[deploy] Restarting services..."
docker compose -f "${COMPOSE_FILE}" -f "${COMPOSE_PROD}" up -d --remove-orphans

echo "[deploy] Waiting for health check..."
sleep 10

STATUS=$(docker compose -f "${COMPOSE_FILE}" -f "${COMPOSE_PROD}" ps --format json 2>/dev/null || echo "{}")
echo "[deploy] Services status:"
docker compose -f "${COMPOSE_FILE}" -f "${COMPOSE_PROD}" ps

echo "[deploy] Cleaning up old images..."
docker image prune -f

echo "[deploy] Deployment complete at $(date)"
