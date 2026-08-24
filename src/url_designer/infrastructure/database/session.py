from sqlmodel import Session, create_engine
from url_designer.infrastructure.database.config import get_database_url

DATABASE_URL=get_database_url()

engine=create_engine(
    DATABASE_URL,
    echo=True,

)

def get_session():
    with Session(engine)as session:
        yield session
