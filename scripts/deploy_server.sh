#!/usr/bin/env bash

set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/tool_aggregator}"
CODE_DIR="${CODE_DIR:-$APP_DIR/code}"
VENV_DIR="${VENV_DIR:-$APP_DIR/venv}"
APP_ENV_FILE="${APP_ENV_FILE:-$APP_DIR/.env}"
BRANCH="${BRANCH:-main}"
REMOTE_NAME="${REMOTE_NAME:-origin}"
APP_USER="${APP_USER:-www-data}"
GUNICORN_SERVICE="${GUNICORN_SERVICE:-gunicorn}"
NGINX_SERVICE="${NGINX_SERVICE:-nginx}"
CLOUDFLARED_SERVICE="${CLOUDFLARED_SERVICE:-cloudflared}"
RESTART_CLOUDFLARED="${RESTART_CLOUDFLARED:-auto}"
RUN_PIP_INSTALL="${RUN_PIP_INSTALL:-1}"
RUN_MIGRATE="${RUN_MIGRATE:-1}"
RUN_COLLECTSTATIC="${RUN_COLLECTSTATIC:-1}"
RUN_CHECK="${RUN_CHECK:-1}"

log() {
    printf '[deploy] %s\n' "$*"
}

fail() {
    printf '[deploy] ERROR: %s\n' "$*" >&2
    exit 1
}

require_path() {
    local path="$1"
    local label="$2"
    [ -e "$path" ] || fail "$label not found: $path"
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || fail "command not found: $1"
}

run_privileged() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        fail "need root or sudo to run: $*"
    fi
}

systemctl_service_exists() {
    systemctl list-unit-files "${1}.service" --no-legend 2>/dev/null | grep -q "^${1}\.service"
}

restart_service_if_present() {
    local service="$1"
    if systemctl_service_exists "$service"; then
        log "Restarting service: $service"
        run_privileged systemctl restart "$service"
    else
        log "Skipping missing service: $service"
    fi
}

show_service_status_if_present() {
    local service="$1"
    if systemctl_service_exists "$service"; then
        run_privileged systemctl --no-pager --full status "$service" | sed -n '1,12p'
    fi
}

main() {
    require_cmd git
    require_cmd systemctl
    require_path "$CODE_DIR" "code directory"
    require_path "$VENV_DIR/bin/activate" "virtualenv activate script"
    require_path "$APP_ENV_FILE" "env file"

    if [ ! -w "$CODE_DIR" ]; then
        fail "current user cannot write to $CODE_DIR"
    fi

    log "Deploying branch $BRANCH from $REMOTE_NAME in $CODE_DIR"
    cd "$CODE_DIR"

    git fetch "$REMOTE_NAME" "$BRANCH"
    git checkout "$BRANCH"
    git pull --ff-only "$REMOTE_NAME" "$BRANCH"

    # shellcheck disable=SC1090
    source "$VENV_DIR/bin/activate"
    set -a
    # shellcheck disable=SC1090
    source "$APP_ENV_FILE"
    set +a

    if [ "$RUN_PIP_INSTALL" = "1" ] && [ -f requirements.txt ]; then
        log "Installing Python dependencies"
        pip install -r requirements.txt
    fi

    if [ "$RUN_CHECK" = "1" ]; then
        log "Running Django system checks"
        python manage.py check --deploy
    fi

    if [ "$RUN_MIGRATE" = "1" ]; then
        log "Applying database migrations"
        python manage.py migrate --noinput
    fi

    if [ "$RUN_COLLECTSTATIC" = "1" ]; then
        log "Collecting static files"
        python manage.py collectstatic --noinput
    fi

    log "Ensuring code ownership for $APP_USER"
    if id "$APP_USER" >/dev/null 2>&1; then
        run_privileged chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    else
        log "Skipping chown because user does not exist: $APP_USER"
    fi

    restart_service_if_present "$GUNICORN_SERVICE"
    restart_service_if_present "$NGINX_SERVICE"

    case "$RESTART_CLOUDFLARED" in
        1|true|yes|always)
            restart_service_if_present "$CLOUDFLARED_SERVICE"
            ;;
        auto)
            if systemctl_service_exists "$CLOUDFLARED_SERVICE"; then
                restart_service_if_present "$CLOUDFLARED_SERVICE"
            else
                log "Cloudflared service not present; skipping"
            fi
            ;;
        *)
            log "Skipping cloudflared restart"
            ;;
    esac

    log "Service status summary"
    show_service_status_if_present "$GUNICORN_SERVICE"
    show_service_status_if_present "$NGINX_SERVICE"
    show_service_status_if_present "$CLOUDFLARED_SERVICE"

    log "Deployment finished"
}

main "$@"
