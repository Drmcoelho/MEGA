#!/usr/bin/env bash
# Exemplo: marcar issues ativas
for i in 2 3 4 5; do
  gh issue edit $i --add-label "status:in-progress"
done