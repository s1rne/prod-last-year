import os

port = int(os.getenv("PORT", "8000"))
host = os.getenv("HOST", "0.0.0.0")

postgres = {
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "test"),
}
DATABASE_URL = f"postgresql+asyncpg://{postgres['user']}:{postgres['password']}@{
    postgres['host']}:{postgres['port']}/{postgres['database']}"

RANDOM_SECRET = os.getenv("RANDOM_SECRET", "secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 24
