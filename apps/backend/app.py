# Version 1.1.0 - OIDC CI/CD Verified
import os
import socket
from flask import Flask, jsonify
import redis # pyright: ignore[reportMissingImports]

app = Flask(__name__)

# 12-Factor Environment Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Redis Client with short connection timeout
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    socket_connect_timeout=2,
    decode_responses=True
)

@app.route("/")
def index():
    """Main business logic endpoint that increments Redis hit counter."""
    try:
        hits = r.incr("hits")
        return jsonify({
            "status": "success",
            "message": "Enterprise GitOps Microservice API",
            "hits": hits,
            "pod": socket.gethostname(),
            "redis_host": REDIS_HOST
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Redis connection failed",
            "error": str(e),
            "pod": socket.gethostname()
        }), 500

@app.route("/healthz")
def healthz():
    """Kubernetes Liveness Probe: Verifies API process is alive."""
    return jsonify({"status": "healthy"}), 200

@app.route("/readyz")
def readyz():
    """Kubernetes Readiness Probe: Verifies Redis dependency before accepting traffic."""
    try:
        r.ping()
        return jsonify({"status": "ready", "redis": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not_ready", "error": str(e)}), 503

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
