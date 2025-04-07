from sqlmodel import SQLModel, create_engine, Session

connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///./test.db", connect_args=connect_args)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session