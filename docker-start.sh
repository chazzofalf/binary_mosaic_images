#!/bin/bash
. /etc/.venv/bin/activate
export DOCKER_EXT_ARG_FFMPEG_EXECUTABLE_PATH="$(which ffmpeg)"
python3 /etc/pydo.py