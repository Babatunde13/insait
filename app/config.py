import os
import dotenv

dotenv.load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@db/ai_text_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    PORT = os.getenv("PORT", 5001)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    ISTESTING = False
    USE_AI_MOCK = os.getenv("USE_AI_MOCK") is not None

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "postgresql://user:password@db/ai_text_db")
    FLASK_ENV = "testing"
    ISTESTING = True
    USE_AI_MOCK = True

config = Config() if os.getenv("FLASK_ENV") != "testing" else TestConfig()
