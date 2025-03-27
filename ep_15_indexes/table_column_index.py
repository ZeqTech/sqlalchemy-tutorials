# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# https://www.youtube.com/watch?v=WsDVBEmTlaI


# When you run this code, you can see the line in the output:

# sqlalchemy.engine.Engine CREATE UNIQUE INDEX ix_users_email ON users (email)


from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)  # Add the index here


Base.metadata.create_all(engine)
