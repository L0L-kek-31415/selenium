#!/bin/sh

echo "Waiting for browser..."

while ! nc -z 'browser' '4444'; do
  sleep 0.1
done

echo "Browser started"

echo "Waiting for rabbit..."

while ! nc -z 'rabbit' '5672'; do
  sleep 0.1
done

echo "Browser rabbit"

python3 start.py --workers 6 --pages 2 --database mongo
#python3 /app/parser/subreddit_parser/subreddit.py
#python3 /app/parser/queue.py


exec "$@"