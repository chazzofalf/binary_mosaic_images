#!/bin/bash
export DEBIAN_FRONTEND="noninteractive"
apt update || exit 1
apt dist-upgrade -yq || exit 2
apt install python3.11 python3.11-venv python3-pip ffmpeg -yq || exit 3
mkdir /src/
mkdir /temp/
mkdir /temp/in
mkdir /temp/out
python3 -m venv --copies --clear --upgrade-deps /etc/.venv || exit 4
. /etc/.venv/bin/activate || exit 5
cd /src
pip install . || exit 6
chmod +x /etc/docker-start.sh

