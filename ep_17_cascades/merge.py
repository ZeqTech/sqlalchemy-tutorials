from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = 'parents'
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List['Child']] = relationship(
        back_populates='parent', cascade='save-update, merge'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child id: {self.id} parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Create and commit parent and child
session = SessionLocal()
parent = Parent(children=[Child()])
session.add(parent)
session.commit()
print(f"Original committed parent: {parent}")
session.close()

# Since the session was closed, the parent is now detatched.
# Add a new child while detached
parent.children.append(Child())

# Merge back into a new session
session = SessionLocal()
merged = session.merge(parent)  # Merges the updated object
print(f"Merged parent in session: {merged}")
session.commit()

# Query to confirm children were merged
fetched = session.query(Parent).first()
print(f"Fetched from DB: {fetched}")
session.close()
