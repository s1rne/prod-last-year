import os

SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")
# POSTGRES_CONN = os.getenv("POSTGRES_CONN")
# POSTGRES_JDBC_URL = os.getenv("POSTGRES_JDBC_URL")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "test")
RANDOM_SECRET = os.getenv("RANDOM_SECRET", "secret")

if SERVER_ADDRESS:
    if ":" in SERVER_ADDRESS:
        host, port = SERVER_ADDRESS.split(":")
        if port != SERVER_PORT:
            port = SERVER_PORT
    else:
        host = SERVER_ADDRESS
        port = SERVER_PORT
else:
    host = "0.0.0.0"
    port = SERVER_PORT
port = int(port)

db_url = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{
    POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 24
