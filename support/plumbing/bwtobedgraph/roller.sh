#! /bin/bash
set -e  # exit if any exception

python roller.py $1

echo "${1} rolled"

