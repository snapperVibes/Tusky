#! /usr/bin/env bash
set -e
python /src/scripts/_tests_pre_start.py

pytest app/tests "${@}"
