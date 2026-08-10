from flask import Blueprint, request, jsonify
import os
import tempfile

from controllers.analysis_controller import analyze_log_file
from parsers.combined_parser import CombinedParser
from parsers.common_parser import CommonParser


analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.post("/analyze")
def analyze_route():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "Log file is required"
        }), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    parser_type = request.form.get("parser_type")

    if parser_type == "common":
        parser = CommonParser()

    elif parser_type == "combined":
        parser = CombinedParser()

    else:
        return jsonify({
            "success": False,
            "message": "Invalid parser type"
        }), 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as temp_file:
            uploaded_file.save(temp_file.name)
            temp_path = temp_file.name
        
        analysis_result = analyze_log_file(temp_path, parser)

        return jsonify({
            "success": True,
            "analysis": analysis_result 
        }), 200
    
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
