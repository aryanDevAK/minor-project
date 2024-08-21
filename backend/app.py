from flask import Flask
from config import ApplicationConfig
from models.dbConfig import db
from routes.register import register_bp

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

db.init_app(app)

app.register_blueprint(register_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)