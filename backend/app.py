from flask import Flask
from config import ApplicationConfig
from models.dbConfig import db
from routes.register import register_doc_bp, register_dept_bp, register_nurse_bp, register_room_bp, register_staff_bp, register_lab_bp, register_patient_bp
from routes.assignment import register_assign_doc_dept_bp, register_assign_nurse_dept_bp
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
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)


app.register_blueprint(register_doc_bp)
app.register_blueprint(register_dept_bp)
app.register_blueprint(register_nurse_bp)
app.register_blueprint(register_staff_bp)
app.register_blueprint(register_room_bp)
app.register_blueprint(register_lab_bp)
app.register_blueprint(register_patient_bp)
app.register_blueprint(register_assign_doc_dept_bp)
app.register_blueprint(register_assign_nurse_dept_bp)
app.register_blueprint(login_bp)
app.register_blueprint(login_patient_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)