#!/bin/sh

set -e

echo "Initiating docker compose"
docker compose --env-file ./config/common.env down --remove-orphans
docker compose --env-file ./config/common.env build
docker compose --env-file ./config/common.env up --remove-orphans
