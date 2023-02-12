from database import SessionLocal, engine


def get_db():
    """doc"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
