from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_09_raise_database.db"

engine = create_engine(db_url, echo=True) # important

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sensitive_information = relationship('SensitiveInformation', backref='user', lazy='raise')

    def __repr__(self):
        return f'<User {self.name} >'

class SensitiveInformation(Base):
    __tablename__ = 'sensitive_informations'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    session.add_all(
        [
            User(
                name=f"User {y}",
                sensitive_information=[
                    SensitiveInformation(
                        content=f"This is sensitive information for {y * 2 + x}"
                    )
                    for x in range(2)
                ]
            ) for y in range(10)
        ]
    )

users = session.query(User).all()
for user in users:
    print(user.name)
    try:
        for information in user.sensitive_information :  # This will raise an exception
            print(information.content)
    except Exception as e:
        print("Posts cannot be accessed directly:", e)
