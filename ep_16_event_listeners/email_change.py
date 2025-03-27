# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=_cHSW_ehjtY

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


user = User(name='User 1', email='user_1@example.com')
session.add(user)
session.commit()


# Add an event through a decorator
@event.listens_for(User, 'before_update')
def audit_user_update(mapper: Mapper, connection: Connection, target: User):
    stmt = text('SELECT email FROM users WHERE id = :user_id')
    old_email = connection.scalar(stmt, {'user_id': target.id})
    new_email = target.email
    if new_email != old_email:
        print(f'Email changed for user {target.id}: {old_email} -> {new_email}')


user = session.query(User).filter_by(name='User 1').first()
user.email = 'user_updated@example.com'
session.commit()
