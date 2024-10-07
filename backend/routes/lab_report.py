import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.Lab_Report import Lab_Report, generate_custom_id
from models.Patient_Test_Report import Patient_Test_Report
from models.patient import Patient
from models.lab import Lab
import sqlalchemy.exc

# Blueprint for lab report routes
lab_report_bp = Blueprint('lab_report', __name__)

# Define the folder to store uploaded PDF files
UPLOAD_FOLDER = 'uploads/reports'  # Adjust this to your folder path
ALLOWED_EXTENSIONS = {'pdf'}

# Utility function to check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CREATE Operation for uploading a lab report
@lab_report_bp.route('/lab/report', methods=['POST'])
@jwt_required()
def upload_lab_report():
    try:
        # Retrieve form data
        patient_id = request.form.get('patient_id')
        lab_id = request.form.get('lab_id')
        test_name = request.form.get('test_name')

        # File upload (PDF)
        test_report = request.files.get('test_report')

        if not patient_id or not lab_id or not test_name or not test_report:
            return jsonify({"error": "All fields (patient_id, lab_id, test_name, test_report) are required"}), 400

        # Validate if the file is a PDF and secure filename
        if test_report and allowed_file(test_report.filename):
            filename = secure_filename(test_report.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            test_report.save(filepath)  # Save the file to the server

        else:
            return jsonify({"error": "Only PDF files are allowed"}), 400

        # Check if patient and lab exist
        patient = Patient.query.filter_by(id=patient_id).first()
        lab = Lab.query.filter_by(id=lab_id).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        if not lab:
            return jsonify({"error": "Lab not found"}), 404

        # Create new lab report entry
        new_report = Lab_Report(
            test_report=filepath,  # Store file path
            test_name=test_name
        )
        db.session.add(new_report)
        db.session.flush()  # Get new_report.id

        # Create Patient_Test_Report association
        patient_test_report = Patient_Test_Report(
            patient_id=patient_id,
            lab_id=lab_id,
            report_id=new_report.id
        )
        db.session.add(patient_test_report)
        db.session.commit()

        return jsonify({"message": "Lab report uploaded successfully", "report_id": new_report.id}), 201

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# READ Operation (Get all reports for a Patient)
@lab_report_bp.route('/lab/reports/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_reports_by_patient(patient_id):
    try:
        # Validate patient existence
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Fetch all reports for the patient
        reports = db.session.query(Lab_Report).join(
            Patient_Test_Report, Lab_Report.id == Patient_Test_Report.report_id
        ).filter(Patient_Test_Report.patient_id == patient_id).all()

        if not reports:
            return jsonify({"message": "No reports found for this patient"}), 404

        # Serialize reports
        report_list = [{
            "id": report.id,
            "test_name": report.test_name,
            "test_date": report.test_date.strftime('%Y-%m-%d'),
            "file_path": report.test_report  # The path to the report file
        } for report in reports]

        return jsonify(report_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE Operation (Update test name or replace report)
@lab_report_bp.route('/lab/report/<string:report_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_lab_report(report_id):
    try:
        # Fetch the report by ID
        report = Lab_Report.query.filter_by(id=report_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404

        # Update test name if provided
        test_name = request.form.get('test_name')
        if test_name:
            report.test_name = test_name

        # If a new test report file is provided, replace the existing file
        new_report_file = request.files.get('test_report')
        if new_report_file and allowed_file(new_report_file.filename):
            new_filename = secure_filename(new_report_file.filename)
            new_filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            new_report_file.save(new_filepath)

            # Optionally, delete the old file if no longer needed
            if os.path.exists(report.test_report):
                os.remove(report.test_report)

            # Update report path in the database
            report.test_report = new_filepath

        db.session.commit()

        return jsonify({"message": "Lab report updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE Operation (Delete a lab report)
@lab_report_bp.route('/lab/report/<string:report_id>', methods=['DELETE'])
@jwt_required()
def delete_lab_report(report_id):
    try:
        # Fetch the report by ID
        report = Lab_Report.query.filter_by(id=report_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404

        # Delete the associated report file from the filesystem
        if os.path.exists(report.test_report):
            os.remove(report.test_report)

        # Delete the report from the database
        db.session.delete(report)
        db.session.commit()

        return jsonify({"message": "Lab report deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
