from sqlalchemy import Column, ForeignKey, String, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, defer, deferred,
                            mapped_column, sessionmaker, undefer,
                            undefer_group)

engine = create_engine("sqlite:///database.db", echo=True)
session = sessionmaker(bind=engine)()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = deferred(mapped_column(String))
    last_name = deferred(Column(String))
    other_value: Mapped[str] = mapped_column(String, deferred=True)

    def __repr__(self) -> str:
        return f"< User: {self.id} - {self.nickname} >"


# Create the database tables
Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    user = User(
        nickname="ZT",
        first_name="Zeq",
        last_name="Tech",
        other_value="secret value"
    )
    session.add(user)
    session.commit()


# undefer nothing
print("\nUndefer Nothing")
user = session.query(User).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

# close the session to show deferring
session.close()

print("\nUndefer One Column")
# undefer one column
user = session.query(User).options(undefer(User.first_name)).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

# close the session to show deferring
session.close()

print("\nUndefer One Column")
user = session.query(User).options(undefer(User.last_name)).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)

# close the session to show deferring
session.close()

print("\nUndefer Multiple Column")
# undefer multiple columns
user = session.query(User).options(undefer(User.last_name), undefer(User.other_value)).first()
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)
