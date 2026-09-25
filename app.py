"""
Vyaapti Test-Triage Copilot Web Application
=============================================
Flask server for live demonstration on Replit, Render, or local development.
"""

from flask import Flask, send_from_directory, jsonify
import subprocess
import os
import json

app = Flask(__name__, static_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/compliance")
@app.route("/compliance.html")
def compliance_page():
    return send_from_directory(".", "compliance.html")

@app.route("/risk_chains")
@app.route("/risk_chains.html")
def risk_chains_page():
    return send_from_directory(".", "risk_chains.html")

@app.route("/governance")
@app.route("/governance.html")
def governance_page():
    return send_from_directory(".", "governance.html")

@app.route("/api/run-tests")
def api_run_tests():
    try:
        res = subprocess.run(["python", "run_tests.py"], capture_output=True, text=True)
        return jsonify({
            "returncode": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/compliance-report")
def api_compliance():
    try:
        with open("COMPLIANCE_INCIDENT_REPORT.txt", "r", encoding="utf-8") as f:
            return jsonify({"report": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/replay-audit")
def api_replay():
    try:
        subprocess.run(["python", "replay_audit.py"], capture_output=True, text=True)
        with open("MISSED_TRANSACTIONS_STR_MANIFEST.json", "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Vyaapti Mission Control running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
