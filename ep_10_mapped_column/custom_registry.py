# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================

from typing import Optional

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from typing_extensions import Annotated

engine = create_engine('sqlite:///ep_10_custom_registry.db', echo=True)

str_20 = Annotated[str, 20]
str_100 = Annotated[str, 100]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_20: String(20),
            str_100: String(100),
        }
    )


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str_20]]
    last_name: Mapped[Optional[str_100]]


# Create the database tables
Base.metadata.create_all(engine)
