import os

class Config:
    # ======================
    # Database Configuration
    # ======================
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing.\n"
            "Please add it in Vercel → Settings → Environment Variables\n"
            "and make sure it is enabled for Production + Preview."
        )

    # Convert to SQLAlchemy + psycopg3 format
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # Recommended for Vercel (serverless)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 2,
        "connect_args": {
            "connect_timeout": 10,
            "options": "-c timezone=Asia/Kolkata"
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ======================
    # Security
    # ======================
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is missing.\n"
            "Please add it in Vercel → Settings → Environment Variables."
        )

    # ======================
    # Session Settings
    # ======================
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 days
