from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.get("/metrics")
def get_metrics():
    result = {}
    for key in r.scan_iter("metrics:*"):
        content_id = key.split(":")[1]
        result[content_id] = r.hgetall(key)
    return result
