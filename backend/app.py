import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
import requests

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
SMARTGUIDE_API_URL = os.getenv("SMARTGUIDE_API_URL", "").rstrip("/")

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")


def proxy(path, method="GET", payload=None, params=None):
    if not SMARTGUIDE_API_URL:
        return None, "SmartGuide connector is not configured"
    url = f"{SMARTGUIDE_API_URL}{path}"
    try:
        r = requests.request(method, url, json=payload, params=params, timeout=20)
        try:
            data = r.json()
        except ValueError:
            data = {"raw": r.text}
        return (data, r.status_code), None
    except requests.RequestException as exc:
        return None, f"SmartGuide connector unavailable: {exc.__class__.__name__}"


@app.get("/api/health")
def health():
    result, error = proxy("/api/v8/health")
    if result:
        data, status = result
        return jsonify({"smarthub": "healthy", "connector": "connected", "smartguide": data}), status
    return jsonify({"smarthub": "healthy", "connector": "not_configured", "message": error}), 200


@app.post("/api/copilot")
def copilot():
    body = request.get_json(silent=True) or {}
    message = str(body.get("message") or "").strip()
    role = str(body.get("role") or "general")
    if not message:
        return jsonify({"error": "message is required"}), 400
    result, error = proxy("/api/v8/agent/orchestrate", "POST", {"message": message, "role": role})
    if result:
        data, status = result
        return jsonify({"source": "SmartGuide", "data": data}), status
    return jsonify({
        "source": "SmartHub",
        "status": "connector_required",
        "message": error,
        "next": "Set SMARTGUIDE_API_URL to the deployed SmartGuide API."
    }), 503


@app.post("/api/product-intelligence")
def product_intelligence():
    body = request.get_json(silent=True) or {}
    result, error = proxy("/api/v8/product-intelligence", "POST", body)
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"error": error, "status": "connector_required"}), 503


@app.get("/api/labs")
def labs():
    query = request.args.to_dict()
    result, error = proxy("/api/v8/labs/match", "GET", params=query)
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"error": error, "status": "connector_required"}), 503


@app.post("/api/scan")
def scan():
    body = request.get_json(silent=True) or {}
    result, error = proxy("/api/v8/qr/decode", "POST", body)
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"error": error, "status": "connector_required"}), 503


@app.post("/api/report")
def report():
    body = request.get_json(silent=True) or {}
    result, error = proxy("/api/v8/reports/suspicious", "POST", body)
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"error": error, "status": "connector_required"}), 503


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/<path:path>")
def static_files(path):
    target = FRONTEND / path
    if target.exists() and target.is_file():
        return send_from_directory(FRONTEND, path)
    return send_from_directory(FRONTEND, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
