#!/bin/bash
apt update
apt dist-upgrade -yq
apt install python-3.11 python-3.11-venv python3-pip ffmpeg
mkdir /etc/.venv
mkdir /src/
mkdir /temp/
mkdir /temp/in
mkdir /temp/out
python3 -m venv --copies --clear --upgrade-deps /etc/.venv
. /etc/.venv/bin/activate
cd /src
pip install .
chmod +x /etc/docker-start.sh

