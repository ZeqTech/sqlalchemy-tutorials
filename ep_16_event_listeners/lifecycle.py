# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=_cHSW_ehjtY


from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


# Define a simple User model
class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Event Listener Functions
def log_event(name):
    """Decorator to log SQLAlchemy events"""

    def wrapper(*args, **kwargs):
        print(f'🔹 {name} triggered!')

    return wrapper


# Session Lifecycle Events
event.listen(Session, 'before_flush', log_event('before_flush'))
event.listen(Session, 'after_flush', log_event('after_flush'))
event.listen(Session, 'after_flush_postexec', log_event('after_flush_postexec'))
event.listen(Session, 'before_commit', log_event('before_commit'))
event.listen(Session, 'after_commit', log_event('after_commit'))
event.listen(Session, 'after_rollback', log_event('after_rollback'))

#  Object Lifecycle (Mapper) Events
event.listen(User, 'before_insert', log_event('before_insert'))
event.listen(User, 'after_insert', log_event('after_insert'))
event.listen(User, 'before_update', log_event('before_update'))
event.listen(User, 'after_update', log_event('after_update'))
event.listen(User, 'before_delete', log_event('before_delete'))
event.listen(User, 'after_delete', log_event('after_delete'))

# Execution Events
event.listen(engine, 'before_execute', log_event('before_execute'))
event.listen(engine, 'after_execute', log_event('after_execute'))

# Transaction Test Cases
try:
    print('\nINSERT OPERATION')
    user = User(name='Zeq')
    session.add(user)
    session.flush()
    session.commit()

    print('\nQuery OPERATION')
    u = session.query(User).all()
    print('\nQuery OPERATION')
    u = session.execute(select(User)).all()
    print('\nQuery OPERATION')
    u = session.scalar(select(User))

    print('\nUPDATE OPERATION')
    user.name = 'Zeq Updated'
    session.flush()
    session.commit()

    print('\nUPDATE OPERATION')
    user.name = 'Zeq Updated'
    session.flush()

    print('\nDELETE OPERATION')
    session.delete(user)
    session.flush()
    session.commit()

    print('\nROLLBACK OPERATION')
    user1 = User(name='Zeq')
    session.add(user1)

    user2 = User(name='Zeq')  # 🚨 Violates UNIQUE constraint
    session.add(user2)
    session.commit()  # This will fail!

except Exception as e:
    print(f'❌ Error: {e}')
    session.rollback()
