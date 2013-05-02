#!/bin/sh
cut -f2 | rev | cut -d. -f-2 | rev | sort | uniq -c | sort -nr
