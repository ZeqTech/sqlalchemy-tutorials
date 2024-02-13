from sqlalchemy import URL, create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import declarative_base

url_object = URL.create(
    "sqlite",
    database="ep_02_database.db",
)
# or
# engine = create_engine("sqlite:///ep_02_database.db.db")

# Create an engine for a SQLite database
engine = create_engine(url_object)

# Create a base class for our models
Base = declarative_base()

# Define a model for the "users" table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self) -> str:
        return f"<User id: {self.id:>3}: name: {self.name:<13}, age: {self.age:>3}>"

# create the database tables
Base.metadata.create_all(engine)
