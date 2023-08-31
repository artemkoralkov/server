import os

class Config:
    POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
    SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")
    POSTGRES_DATABASE_URLd = os.getenv("POSTGRES_DATABASE_URLd")


settings = Config()
