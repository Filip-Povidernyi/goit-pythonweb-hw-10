class Config:
    DB_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/db_app"
    JWT_SECRET = "secret"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600


config = Config
