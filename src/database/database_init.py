from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL: str = "mysql+pymysql://root:admin@127.0.0.1:3306/lessonlink"


engine = create_engine(
    DATABASE_URL, future=True,
    pool_size=500, max_overflow=500, pool_timeout=30, pool_recycle=3600,
)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
