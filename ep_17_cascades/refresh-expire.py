from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update, refresh-expire'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

print("\nBefore Expire:")
print(parent.children) 
print(parent.children) 
session.expire(parent)
# session.expire_all([parent])

# Re-fetches from DB if accessed
print("\nAfter Expire:")
print(parent.children) 
