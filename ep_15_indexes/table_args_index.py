# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# https://www.youtube.com/watch?v=WsDVBEmTlaI


# When you run this code, you can see the line in the output:
# sqlalchemy.engine.Engine CREATE UNIQUE INDEX ix_users_email ON users (email)


from sqlalchemy import Index, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)  # Add the index here

    __table_args__ = (
        # The first argument is the index name and the second argument is the column name we want to use
        # here we just put the string representation of the column name
        # Be sure to add a comma to make the __table_args__ a tuple
        Index('ix_users_name', 'name'),
    )


Base.metadata.create_all(engine)
