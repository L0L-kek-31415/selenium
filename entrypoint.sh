#!/bin/sh

echo "Waiting for browser..."

while ! nc -z 'browser' '4444'; do
  sleep 0.1
done

echo "Browser started"

python3 start.py --workers 2 --pages 2

exec "$@"