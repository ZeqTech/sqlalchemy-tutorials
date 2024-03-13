import random

from models import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

names = ["Andrew Pip", "Iron Man", "John Doe", "Jane Doe"]
ages = [20, 21, 22, 23, 25, 27, 30, 35, 60]


# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    # Create random Users
    for x in range(20):
        user = User(name=random.choice(names), age=random.choice(ages))
        session.add(user)

    session.commit()


# Query all users ordered by age (ascending)
users_1 = session.query(User).order_by(User.age).all()
# this is the same as:
# users_1 = session.query(User).order_by(User.age.asc()).all()

print('\nAll Users Ordered by age (ascending)')
for user in users_1:
    print(user)

# Query all users ordered by age (descending)
users_2 = session.query(User).order_by(User.age.desc()).all()
print('\nAll Users Ordered by age (descending)')
for user in users_2:
    print(user)

# Order first by age and then name
users = session.query(User).order_by(User.age, User.name).all()
print('\nAll Users Ordered by age (ascending) and then name(ascending)')
for user in users:
    print(user)
