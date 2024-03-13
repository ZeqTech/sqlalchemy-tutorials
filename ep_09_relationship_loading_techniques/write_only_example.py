from time import perf_counter

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_09_write_only_database.db"

engine = create_engine(db_url, echo=True) # important

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    logs = relationship('Log', backref='user', lazy='write_only')

    def __repr__(self):
        return f'<User {self.name} >'

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'<Log{self.id} >'

Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    session.add_all(
        [
            User(
                name=f"User {y}",
                logs=[
                    Log(
                        message=f"User did this thing"
                    )
                    for x in range(3)
                ]
            ) for y in range(10)
        ]
    )
    session.commit()

users = session.query(User).all()
for user in users:
    print(user.name)
    for post in user.posts:  # Efficiently loads posts for all queried users using a subquery
        print(post.content)
