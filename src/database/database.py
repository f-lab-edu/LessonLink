from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL :str = "mysql+pymysql://root:admin@localhost:3306/lessonlink"


engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
