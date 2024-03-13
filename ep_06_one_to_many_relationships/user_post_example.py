from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_06_user_post_database.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)

class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(String)
    content = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)

    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post (id={self.id}, title='{self.title}')>"


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    age = Column(Integer)
    posts = relationship(Post)

    def __repr__(self):
        return f"<User(id={self.id}, age='{self.age}')>"


Base.metadata.create_all(engine)

session = Session()

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    # Creating user
    user = User(name="Zeq Tech", age=999)

    # Creating addresses
    post = Post(title="Subscribe", content="Subscribe to Zeq Tech!", likes=999, dislikes=0)

    # Associating addresses with users
    user.posts.append(post)

    # Adding users and addresses to the session and committing changes to the database
    session.add(user)
    session.commit()

post = session.query(Post).first()
user = session.query(User).first()

print(f'{post.user = }')
print(f"{user.posts = }")
