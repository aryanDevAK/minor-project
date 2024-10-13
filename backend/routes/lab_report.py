import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from models.dbConfig import db
from models.lab_report import Lab_Report, generate_custom_id
from models.patient_report import Patient_Test_Report
from models.patient import Patient
from models.labs import Lab
import sqlalchemy.exc
from routes.helper_function import str_to_date, has_required_role

lab_report_bp = Blueprint('lab_report', __name__)
UPLOAD_FOLDER = 'uploads/reports'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lab_report_bp.route('/lab/report', methods=['POST'])
@jwt_required()
def upload_lab_report():
    if not has_required_role(["admin","lab"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        patient_id = request.form.get('patient_id')
        lab_id = request.form.get('lab_id')
        test_name = request.form.get('test_name')
        test_report = request.files.get('test_report')

        if not patient_id or not lab_id or not test_name or not test_report:
            return jsonify({"error": "All fields are required"}), 400

        patient = Patient.query.filter_by(id=patient_id).first()
        lab = Lab.query.filter_by(id=lab_id).first()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404
        if not lab:
            return jsonify({"error": "Lab not found"}), 404
        
        if test_report and allowed_file(test_report.filename):
            filename = secure_filename(test_report.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            test_report.save(filepath)
        else:
            return jsonify({"error": "Only PDF files are allowed"}), 400

        new_report = Lab_Report(
            test_report=filepath, 
            test_name=test_name
        )
        db.session.add(new_report)
        db.session.flush()  

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

@lab_report_bp.route('/lab/reports/<string:patient_id>', methods=['GET'])
@jwt_required()
def get_reports_by_patient(patient_id):
    if not has_required_role(["admin","lab","doctor","nurse"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        reports = db.session.query(
            Lab_Report
        ).join(Patient_Test_Report, Lab_Report.id == Patient_Test_Report.report_id) \
         .filter(Patient_Test_Report.patient_id == patient_id) \
         .all()

        if not reports:
            return jsonify({"message": "No reports found for this patient"}), 404

        report_list = [{
            "id": report.id,
            "test_name": report.test_name,
            "test_date": report.test_date.strftime('%Y-%m-%d'),
            "file_path": report.test_report
        } for report in reports]

        return jsonify(report_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lab_report_bp.route('/lab/report/<string:report_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_lab_report(report_id):
    if not has_required_role(["admin","lab"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        report = Lab_Report.query.filter_by(id=report_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404

        test_name = request.form.get('test_name')
        patient_id = request.form.get("patient_id")

        if test_name:
            report.test_name = test_name

        if patient_id:
            patient = Patient.query.filter_by(id=patient_id).first()
            if patient:
                patient_info = Patient_Test_Report.query.filter_by(report_id=report_id).first()
                if patient_info:
                    patient_info.patient_id = patient_id
                else:
                    return({"message":"No records found"})         
            else:
                return({"message":"Patient not found"})

        new_report_file = request.files.get('test_report')
        if new_report_file and allowed_file(new_report_file.filename):
            new_filename = secure_filename(new_report_file.filename)
            new_filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            new_report_file.save(new_filepath)
            if os.path.exists(report.test_report):
                os.remove(report.test_report)

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
    if not has_required_role(["admin"]):
        return jsonify({"message": "You do not have permission to do that"}), 401
    try:
        report = Lab_Report.query.filter_by(id=report_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404

        if os.path.exists(report.test_report):
            os.remove(report.test_report)

        db.session.delete(report)
        db.session.commit()

        return jsonify({"message": "Lab report deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
