
import redis
import json
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Aggregation service started (incremental)...")

while True:
    # خذ الأحداث الجديدة فقط
    events = r.lpop("latest_events", 10)

    if not events:
        time.sleep(5)
        continue

    if isinstance(events, str):
        events = [events]

    for e in events:
        event = json.loads(e)

        content_id = event.get("content_id")
        event_type = event.get("type")

        if not content_id or not event_type:
            continue

        key = f"metrics:{content_id}"

        # زيادة العد
        r.hincrby(key, event_type, 1)

    print("Processed batch of events")
    time.sleep(5)
