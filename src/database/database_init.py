from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL: str = "mysql+pymysql://root:admin@localhost:3306/lessonlink"
DATABASE_URL_ASYNC: str = "mysql+aiomysql://root:admin@localhost:3306/lessonlink"


engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True, future=True)
AsyncSessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


def get_database():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


async def get_async_database():
    async with AsyncSessionFactory() as session:
        yield session