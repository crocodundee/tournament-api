from environs import Env

env = Env()
env.read_env()

ENVIRONMENT = env.str("ENVIRONMENT")
DEBUG = env.bool("DEBUG", False)
DATABASE_URL = env.str("DATABASE_URL")
JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITHM = env.str("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

# SMTP Settings
SMTP_HOST = env.str("SMTP_HOST", "mailhog")
SMTP_PORT = env.int("SMTP_PORT", 1025)
SMTP_USER = env.str("SMTP_USER", "")
SMTP_PASSWORD = env.str("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = env.str("SMTP_FROM_EMAIL", "noreply@example.com")
