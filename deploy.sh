#!/usr/bin/env bash

set -Eeuo pipefail

if [ ! -f "manage.py" ]; then
    echo "错误: 请在项目根目录运行此脚本" >&2
    exit 1
fi

exec bash scripts/deploy_remote.sh "$@"
