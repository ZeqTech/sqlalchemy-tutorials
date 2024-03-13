from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship, sessionmaker)

db_url = "sqlite:///ep_06_user_self_database.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)

class FollowerAssociation(BaseModel):
    __tablename__ = "follower_association"

    user_id = Column(Integer, ForeignKey('users.id'))
    follower_id = Column(Integer, ForeignKey('users.id'))

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String)
    followers = relationship('User', secondary="follower_association",
                            primaryjoin=("FollowerAssociation.user_id==User.id"),
                            secondaryjoin=("FollowerAssociation.follower_id==User.id"),
                            )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    # Creating users
    user1 = User(username="Zeq Tech 1" )
    user2 = User(username="Zeq Tech 2" )
    user3 = User(username="Zeq Tech 3" )

    # Creating relationships
    user1.followers.append(user2)
    user1.followers.append(user3)
    user2.followers.append(user3)
    user3.followers.append(user1)

    # Adding users to the session and committing changes to the database
    session.add_all([user1, user2, user3])
    session.commit()

user1, user2, user3 = session.query(User).limit(3).all()

print(f"{user1.followers = }")
print(f"{user2.followers = }")
print(f"{user3.followers = }")
