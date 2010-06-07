#!/bin/bash

#clear

set -e

PYTHON=python2.6

cd "$(dirname ${0})/"

BASEDIR="$(pwd)"
GAME_DIR="${BASEDIR}/game"

export PYTHONPATH="${GAME_DIR}"

cd "${BASEDIR}/moo2/"

${PYTHON} ${GAME_DIR}/openmoo2_server.py "$@"
