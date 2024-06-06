# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=iwENqqgxm-g

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from utils import int_big, str_20, str_100

engine = create_engine('sqlite:///ep_10_custom_annotations.db', echo=True)


class Base(DeclarativeBase):
    type_annotation_map = {
        int: int_big,
    }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str_20]]
    last_name: Mapped[Optional[str_100]]


# Create the database tables
Base.metadata.create_all(engine)
