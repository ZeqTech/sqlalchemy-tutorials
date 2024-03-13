from sqlalchemy import Column, ForeignKey, String, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, defer, deferred,
                            mapped_column, sessionmaker, undefer)

engine = create_engine("sqlite:///ep_11_deferred_raiseload.db", echo=True)
session = sessionmaker(bind=engine)()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = deferred(mapped_column(String), raiseload=True)
    last_name = deferred(Column(String), raiseload=True)
    other_value: Mapped[str] = mapped_column(String, deferred=True, deferred_raiseload=True)

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

try:
    # Will raise an error since there is lazy loading
    user = session.query(User).first()
    print(user)
    print(user.first_name)
    print(user.last_name)
    print(user.other_value)
except Exception as e:
    print("*" * 60)
    print(f"Raiseload error:")
    print(e)
    print("*" * 60)

try:
    # Will raise an error since there is lazy loading
    user = session.query(User).options(undefer(User.first_name), undefer(User.last_name)).first()
    print(user)
    print(user.first_name)
    print(user.last_name)
    print(user.other_value)
except Exception as e:
    print("*" * 60)
    print(f"Raiseload error:")
    print(e)
    print("*" * 60)

# close the session to show deferring
session.close()

# Undefer all values so raiseload doesnt raise an error
user = (
    session
    .query(User)
    .options(
        undefer(User.first_name),
        undefer(User.last_name),
        undefer(User.other_value),
    )
    .first()
)
print(user)
print(user.first_name)
print(user.last_name)
print(user.other_value)
