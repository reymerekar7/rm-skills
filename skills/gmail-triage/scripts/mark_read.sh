#!/usr/bin/env bash
# Mark one or more Gmail messages as read.
#
# Usage:
#   ./mark_read.sh MSG_ID1 MSG_ID2 MSG_ID3 ...
#
# Example:
#   ./mark_read.sh 19cdc65f719df15b 19cdc990d7579945

if [ $# -eq 0 ]; then
  echo "Usage: $0 <message_id> [message_id ...]"
  exit 1
fi

success=0
fail=0

for id in "$@"; do
  result=$(gws gmail users messages modify \
    --params "{\"userId\":\"me\",\"id\":\"$id\"}" \
    --json '{"removeLabelIds":["UNREAD"]}' 2>&1)
  if echo "$result" | grep -q '"id"'; then
    ((success++))
  else
    ((fail++))
    echo "FAILED: $id — $result"
  fi
done

echo "Done: $success marked as read, $fail failed"
