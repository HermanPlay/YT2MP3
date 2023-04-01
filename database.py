from sqlalchemy import Integer, create_engine, String, ForeignKey, Column
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    uid = Column("uid", Integer, primary_key=True)
    chat_id = Column("chat_id", Integer)
    username = Column("username", String)
    firstname = Column("firstname", String)

    def __init__(self, uid: int, chat_id: int, username: str, firstname: str) -> None:
        self.uid = uid
        self.chat_id = chat_id
        self.username = username
        self.firstname = firstname

    def __repr__(self) -> str:
        return f"User {self.firstname} (uid: {self.uid}, username: {self.username}) Chat_id: {self.chat_id}"
    

def get_engine(user="postgres", passwd="herman", host="localhost", port=5432, db="postgres"):
    url = f"postgresql://{user}:{passwd}@{host}/{db}"
    if not database_exists(url):
        create_engine(url)
    return create_engine(url, pool_size=50, echo=False)


engine = get_engine()
# print(engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
print(session)

user = User(123554, 12313453, "Filip", "hermanplay")
session.add(user)

session.commit()