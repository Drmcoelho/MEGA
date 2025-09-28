#!/usr/bin/env bash
echo "Labels existentes:"
gh label list
echo
echo "Issues sem milestone:"
gh issue list --state open --json number,title,milestone | jq -r '.[] | select(.milestone==null) | "\(.number) - \(.title)"'