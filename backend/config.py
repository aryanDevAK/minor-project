class ApplicationConfig:
        
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./medixify.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True