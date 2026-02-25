#!/bin/bash

commit_message="$1"

if [ -z "$commit_message" ]; then
  echo "Please provide a commit message."
  exit 1
fi

echo "$commit_message"
git add .
git commit -m "$commit_message"
git push origin master