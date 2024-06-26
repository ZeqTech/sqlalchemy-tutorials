# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=iwENqqgxm-g

from typing import Optional

from sqlalchemy import Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///ep_10_mapped_columns.db', echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    # column type from the mapped_column function, cannot be null
    id = mapped_column(Integer, primary_key=True)

    # implicit 'mapped_column' createion based off annotation, can be null
    name: Mapped[Optional[str]]

    # column type inferred from the Mapped Annotation, can be null
    age: Mapped[int] = mapped_column(nullable=True)


# Create the database tables
Base.metadata.create_all(engine)
