from models import User, engine
from sqlalchemy import and_, func, not_, or_
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    session.add(User(name="Iron Man", age=23))
    session.add(User(name="Coding Man", age=33))
    session.add(User(name="Banana Man", age=78))
    session.add(User(name="Zeq", age=99))

    session.commit()


# ========================================================================================
print("\nGROUP BY (AGE,)")
users_count_by_age = (
    session.query(User.age).group_by(User.age).all()
)
print(users_count_by_age)

# ========================================================================================
print("\nGROUP BY ADDITIONAL CRITERIA (AGE, COUNT)")
# count the number of users by age
users_count_by_age = session.query(User.age, func.count(User.id)).group_by(User.age).all()
print(users_count_by_age)

# ========================================================================================
print("\nCHAINING METHODS")
users = (
    session.query(User).filter(User.age > 24).filter(User.age < 50).all()
)

for user in users:
    print(f"{user.age = }")

# or like this
users_tuple = (
    session.query(User.age, func.count(User.id))
    .filter(User.age > 24)
    .order_by(User.age)
    .filter(User.age < 50)
    .group_by(User.age)
    .all()
)
for age, count in users_tuple :
    print(f"Age: {age} - Users: {count}")


# ========================================================================================
print("\nDELAY .all()")
only_iron_man = True
group_by_age = True

users = session.query(User)
if only_iron_man:
    users = users.filter(User.name == "Iron Man")
if group_by_age:
    users = users.group_by(User.age)
users = users.all()
for user in users:
    print(f"User age: {user.age}, name: {user.name}")
