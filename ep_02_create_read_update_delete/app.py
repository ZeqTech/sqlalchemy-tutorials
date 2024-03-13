from models import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# ===================================================================================
# CREATE

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    # Create one new User
    user = User(name='John Doe 1', age=30)
    session.add(user)
    session.commit()

    # Create multiple Users
    user_1 = User(name='John Doe 2', age=30)
    user_2 = User(name='Andrew Pip', age=25)
    user_3 = User(name='Iron Man', age=57)
    user_4 = User(name='Richard Rodriguez', age=25)

    session.add(user_1)
    session.add(user_2)
    session.add_all([user_3, user_4])
    session.commit()

# ===================================================================================
# READ
# query all users
users = session.query(User).all()
print(users)

# Get the first User info
user = users[0]
print(user)
print(user.id)
print(user.name)
print(user.age)

user = session.query(User).filter_by(id=1).one_or_none()
print(user)

# Loop over each User
for user in users:
    print(f"User id: {user.id}, name: {user.name}, age: {user.age}")

# Get first user from the data
user_first = session.query(User).first()
print('First User: ', user_first)


# ===================================================================================
# UPDATE
# update a user's name
user = users[0]
user.name = 'Jane Doe'
session.commit()

# ===================================================================================
# DELETE
# delete a user record
user = users[0]
session.delete(user)
session.commit()
