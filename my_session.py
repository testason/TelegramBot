import tables
from sqlalchemy.orm import Session
__factory = tables.global_init("Project.db")


def create_session() -> Session:
    global __factory
    return __factory()


def my_request(id):
    session = create_session()
    chat = session.query(tables.Chat).filter(tables.Chat.id == id).first()
    return chat