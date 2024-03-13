from time import perf_counter

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_09_database.db"

engine = create_engine(db_url, echo=True) # important

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship('Post', lazy='select', backref="user")

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
                name=f"User {y}",
                posts=[
                    Post(
                        content=f"This is the content for {y * 5 + x}"
                    )
                    for x in range(5)
                ]
            ) for y in range(1_000)
        ]
    )
    session.commit()

print('\n\n')

users = session.query(User).all()

print('\n Accessing Posts specifically')
start = perf_counter()

for user in users:
    user.posts

print(f"Done in: {perf_counter() - start}")
