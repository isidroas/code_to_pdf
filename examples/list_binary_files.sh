#!/usr/bin/env bash
# https://unix.stackexchange.com/questions/46276/finding-all-non-binary-files
find $1 -type f -print0 | xargs --no-run-if-empty -0 -n1 file -Li | awk -F: '/charset=(binary)/ {print $1}'
