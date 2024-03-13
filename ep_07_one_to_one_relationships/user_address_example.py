from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///ep_07_one_to_one_relationships.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = relationship("Address", back_populates="user", uselist=False)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="address")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    new_user = User(name='John Doe')
    new_address = Address(email='john@example.com', user=new_user)
    session.add(new_user)
    session.add(new_address)
    session.commit()

user = session.query(User).filter_by(name='John Doe').first()
print(f"User: {user.name}, Address: {user.address.email}")
