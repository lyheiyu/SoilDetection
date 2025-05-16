# This is the main Flask backend file (app.py) for soil data upload and mapping.

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
from utils.convert_csv import csv_to_geojson

# Serve frontend from ../frontend
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    if filename.endswith(".csv"):
        geojson_path = csv_to_geojson(filepath)
    else:
        return jsonify({"status": "Unsupported format"}), 400

    return jsonify({"status": "success", "geojson": f"/data/{os.path.basename(geojson_path)}"})

@app.route("/data/<path:filename>")
def data_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/download/<layer>")
def download_layer(layer):
    filepath = os.path.join(UPLOAD_DIR, layer)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"status": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
