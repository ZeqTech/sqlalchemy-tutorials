from time import perf_counter

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_09_dynamic_database.db"

engine = create_engine(db_url, echo=True) # important

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship('Post', backref='user', lazy='dynamic')

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
    session.add(
        User(
            name="Zeq",
            posts=[
                Post(
                    content=f"Content {x}"
                ) for x in range(50)
            ]
        )
    )
    session.commit()

user = session.query(User).filter_by(name='Zeq').first()
print(user.posts)

recent_posts = user.posts.order_by(Post.id.desc()).limit(10).all()
for post in recent_posts:
    print(post.content)
