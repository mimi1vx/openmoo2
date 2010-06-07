#!/bin/bash

set -e

PYTHON=python2.6

cd "$(dirname ${0})/"

BASEDIR="$(pwd)"
GAME_DIR="${BASEDIR}/game"

export PYTHONPATH="${GAME_DIR}"

cd "${GAME_DIR}/"

echo "PWD = $(pwd)"
${PYTHON} openmoo2.py "$@"
