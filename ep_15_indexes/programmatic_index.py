# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# https://www.youtube.com/watch?v=WsDVBEmTlaI


# When you run this code, you can see the line in the output:

# sqlalchemy.engine.Engine CREATE INDEX ix_users_name ON users (name)
# ...
# DROP INDEX ix_users_name


from sqlalchemy import create_engine, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)

# Add an index programmatically here
user_name_index = Index('ix_users_name', User.name)
user_name_index.create(bind=engine)
user_name_index.drop(bind=engine)
user_name_index.drop(bind=engine, checkfirst=True)
