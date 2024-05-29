# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    deferred,
    mapped_column,
    sessionmaker,
    undefer_group,
)

engine = create_engine('sqlite:///ep_11_deferred_group.db', echo=True)
session = sessionmaker(bind=engine)()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    nickname: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = deferred(mapped_column(String), group='name')
    last_name = deferred(Column(String), group='name')
    other_value: Mapped[str] = mapped_column(
        String, deferred=True, deferred_group='other'
    )

    def __repr__(self) -> str:
        return f'< User: {self.id} - {self.nickname} >'


# Create the database tables
Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    user = User(
        nickname='ZT', first_name='Zeq', last_name='Tech', other_value='secret value'
    )
    session.add(user)
    session.commit()


# undefer nothing
user = session.query(User).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

# close the session to show deferring
session.close()

# undefer one group
user = session.query(User).options(undefer_group('name')).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

session.close()
user = session.query(User).options(undefer_group('other')).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

session.close()
# undefer multiple groups
user = (
    session.query(User).options(undefer_group('name'), undefer_group('other')).first()
)
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)
