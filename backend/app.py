from flask import Flask
from config import ApplicationConfig
from models.dbConfig import db
from routes.doctor_route import doctor_routes_bp
from routes.dept_routes import dept_routes_bp
from routes.nurse_routes import nurse_routes_bp
from routes.staff_routes import staff_routes_bp
from routes.patient_routes import patient_routes_bp
from routes.appointments import appointment_bp
from routes.room_routes import room_bp
from routes.lab_report import lab_report_bp
from routes.prescription_routes import prescription_bp
from routes.lab_routes import lab_bp
from routes.login import login_bp
from routes.login_patient import login_patient_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

CORS(app)

db.init_app(app)

app.config["JWT_SECRET_KEY"] = "abcdefghijklmnopqrstuvwxyz"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=10)
jwt = JWTManager(app)


app.register_blueprint(doctor_routes_bp)
app.register_blueprint(dept_routes_bp)
app.register_blueprint(nurse_routes_bp)
app.register_blueprint(staff_routes_bp)
app.register_blueprint(room_bp)
app.register_blueprint(lab_report_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(lab_bp)
app.register_blueprint(patient_routes_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(login_bp)
app.register_blueprint(login_patient_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)