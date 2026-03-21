#!/usr/bin/env bash

set -Eeuo pipefail

SERVER_HOST="${SERVER_HOST:-}"
SERVER_USER="${SERVER_USER:-}"
SERVER_PORT="${SERVER_PORT:-22}"
SERVER_APP_DIR="${SERVER_APP_DIR:-/var/www/tool_aggregator}"
SERVER_SCRIPT_PATH="${SERVER_SCRIPT_PATH:-$SERVER_APP_DIR/code/scripts/deploy_server.sh}"
BRANCH="${BRANCH:-main}"
PUSH_FIRST="${PUSH_FIRST:-1}"
SSH_OPTS="${SSH_OPTS:-}"

log() {
    printf '[remote-deploy] %s\n' "$*"
}

fail() {
    printf '[remote-deploy] ERROR: %s\n' "$*" >&2
    exit 1
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || fail "command not found: $1"
}

main() {
    require_cmd git
    require_cmd ssh

    [ -n "$SERVER_HOST" ] || fail "SERVER_HOST is required"
    [ -n "$SERVER_USER" ] || fail "SERVER_USER is required"

    if [ "$PUSH_FIRST" = "1" ]; then
        log "Pushing local branch $BRANCH"
        git push origin "$BRANCH"
    else
        log "Skipping git push because PUSH_FIRST=$PUSH_FIRST"
    fi

    log "Triggering remote deployment on ${SERVER_USER}@${SERVER_HOST}:${SERVER_PORT}"
    ssh $SSH_OPTS -p "$SERVER_PORT" "${SERVER_USER}@${SERVER_HOST}" \
        "APP_DIR='$SERVER_APP_DIR' BRANCH='$BRANCH' bash '$SERVER_SCRIPT_PATH'"
}

main "$@"
