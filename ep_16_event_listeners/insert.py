# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=_cHSW_ehjtY

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def insert_user_listener(mapper: Mapper, connection: Connection, target: User):
    print(f'[EVENT: before_insert ] Inserting user: {target.name}')


# Add an event through a function call
event.listen(User, 'before_insert', insert_user_listener)

for x in range(1, 10):
    user = User(name=f'User {x}', email=f'user_{x}@email.com')
    session.add(user)

session.commit()
