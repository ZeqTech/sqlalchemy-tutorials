from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm.exc import DetachedInstanceError


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update, expunge'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(
        back_populates='children', cascade='expunge'
    )

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

session.expunge(parent)

assert parent not in session
# try:
print(parent.children[0])
# except DetachedInstanceError:
#     print('parent.children are not in the session')
