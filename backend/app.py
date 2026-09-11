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
    try:
        r = requests.request(method, f"{SMARTGUIDE_API_URL}{path}", json=payload, params=params, timeout=25)
        try:
            data = r.json()
        except ValueError:
            data = {"raw": r.text}
        return (data, r.status_code), None
    except requests.RequestException as exc:
        return None, f"SmartGuide connector unavailable: {exc.__class__.__name__}"


def require_connector():
    if not SMARTGUIDE_API_URL:
        return jsonify({"status": "connector_required", "message": "Set SMARTGUIDE_API_URL on SmartHub to connect SmartGuide intelligence."}), 503
    return None


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
    return jsonify({"source": "SmartHub", "status": "connector_required", "message": error}), 503


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
    return jsonify({"status": "intake_only", "message": "Suspicious-product reporting is not connected to a live external reporting registry in this deployment. No verification claim was made."}), 202


@app.post("/api/compliance-assessment")
def compliance_assessment():
    body = request.get_json(silent=True) or {}
    product = str(body.get("product") or "").strip()
    if not product:
        return jsonify({"error": "product is required"}), 400
    result, error = proxy("/api/v4/assess", "POST", body)
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"status": "connector_required", "message": error}), 503


@app.get("/api/passport/<assessment_id>")
def passport(assessment_id):
    result, error = proxy(f"/api/v4/passport/{assessment_id}")
    if result:
        data, status = result
        return jsonify(data), status
    return jsonify({"status": "connector_required", "message": error}), 503


@app.get("/api/compliance-workflow")
def compliance_workflow():
    product = str(request.args.get("product") or "").strip()
    if not product:
        return jsonify({"error": "product is required"}), 400
    pi_result, pi_error = proxy("/api/v8/product-intelligence", "POST", {"query": product, "product": product})
    intelligence = pi_result[0] if pi_result else None
    ranked = (intelligence or {}).get("data", {}).get("ranked_standards") or (intelligence or {}).get("ranked_standards") or (intelligence or {}).get("data", {}).get("candidate_standards") or []
    standard = ranked[0] if ranked else None
    standard_number = (standard or {}).get("standard_number", "")
    lab_params = {"product": product}
    if standard_number:
        lab_params["standard"] = standard_number
    lab_result, lab_error = proxy("/api/v8/labs/match", "GET", params=lab_params)
    return jsonify({
        "product": product,
        "stages": [
            {"id": "product", "label": "Product identified", "status": "complete" if intelligence else "blocked", "data": intelligence},
            {"id": "standard", "label": "Applicable BIS standard", "status": "complete" if standard else "needs_review", "data": standard},
            {"id": "requirements", "label": "Requirements & QCO", "status": "next", "action": "Review the standard requirements and current mandatory/QCO status."},
            {"id": "tests", "label": "Required tests", "status": "next", "action": "Map the standard's testing parameters before booking a test."},
            {"id": "lab", "label": "Testing laboratory", "status": "complete" if lab_result else "needs_review", "data": lab_result},
            {"id": "passport", "label": "Compliance Passport", "status": "next", "action": "Generate an evidence-backed assessment after providing checklist/evidence."}
        ],
        "connector": "connected" if intelligence or lab_result else "unavailable",
        "errors": [x for x in [pi_error, lab_error] if x],
        "trust_boundary": "A workflow stage is not certification. Only authoritative evidence may support a verification claim."
    })


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
