# KR2: Gaponov

import os
import socket

from flask import Flask, request
from redis import Redis

app = Flask(__name__)

STUDENT = os.getenv("STUDENT", "unknown")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = Redis(
    host=REDIS_HOST,
    port=6379,
    password=REDIS_PASSWORD,
    decode_responses=True
)


@app.route("/")
def index():
    hits = redis_client.incr("hits")
    container_id = socket.gethostname()

    return f"KR2 | {STUDENT} | container {container_id} | hits: {hits}\n"


@app.route("/health")
def health():
    return "ok\n"


@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")

    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
