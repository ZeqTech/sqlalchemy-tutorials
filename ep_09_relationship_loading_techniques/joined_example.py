from time import perf_counter

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_09_joined_database.db"

engine = create_engine(db_url, echo=True) # important

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latest_post = relationship('Post', uselist=False, lazy='joined')

    def __repr__(self):
        return f'<User {self.name} >'

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.id} >'

Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    session.add_all(
        [
            User(
                name=f"User {x}",
                latest_post=Post(
                        content=f"This is the content for {x}"
                    )
            ) for x in range(10)
        ]
    )
    session.commit()

users = session.query(User).all()
for user in users:
    print(user.name, user.latest_post.content)  # Accessing the latest post directly
