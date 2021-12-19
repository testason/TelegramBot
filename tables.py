import sqlalchemy
import sqlalchemy.ext.declarative as dec
import sqlalchemy as sa
import sqlalchemy.orm as orm

__factory = None


SqlAlchemyBase = dec.declarative_base()


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    language = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.Integer)
    email = sqlalchemy.Column(sqlalchemy.String)


#создание базы данных и/или подключение к ней
def global_init(db_file):
    global __factory
    if __factory:
        return __factory

    if not db_file or not db_file.strip():
        raise Exception("")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключено к базе {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)
    return __factory