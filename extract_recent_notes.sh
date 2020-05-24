#!/bin/sh
# -E means to use extended regexp
# Desire: extract the difference between two files and keep only the notes (remove unnecessary things)
diff -u $1 $2 | grep -E "^\+" | sed -E 's/^\+//' | awk 'NR!=1' >> diff.txt

