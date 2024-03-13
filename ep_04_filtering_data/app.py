from models import User, engine
from sqlalchemy import and_, not_, or_
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    session.add(User(name="Iron Man", age=23))
    session.add(User(name="Coding Man", age=56))
    session.add(User(name="Banana Man", age=78))
    session.add(User(name="Zeq", age=99))

    session.commit()

# query all users
users_all = session.query(User).all()
print('All Users:', len(users_all))


# ========================================================================================
print("\nFILTER")
# query all users with age greater than or equal to 25
users_filtered = session.query(User).filter(User.age >= 25).all()
print('Filtered Users:', len(users_filtered))

# ========================================================================================
print("\nFILTER BY")
# query all users with age is equal to 30
users = session.query(User).filter_by(age=30).all()

for user in users:
    print(f"User age: {user.age}")

# ========================================================================================
print("\nWHERE")
# query all users with age is greater than or equal to 30
users = session.query(User).where(User.age >= 30).all()

for user in users:
    print(f"User age: {user.age}")

# ========================================================================================
print("\nOR")
# query all users with age is greater than or equal to 30 or name is 'Iron Man'
users = session.query(User).where(or_(User.age >= 30, User.name == "Iron Man")).all()
print(f"Users: {len(users)}")

users = session.query(User).where((User.age >= 30) | ( User.name == "Iron Man")).all()
print(f"Users: {len(users)}")

# ========================================================================================
print("\nAND")
# query all users with age is greater than or equal to 30 or name is 'Iron Man'
users = session.query(User).where(and_ (User.age >= 30, User.name == "Iron Man")).all()

print(f"Users: {len(users)}")

# ========================================================================================
print("\nNOT")
# query all users where the name is not 'Iron Man'
users = session.query(User).where(not_(User.name == "Iron Man")).all()

print(f"Users: {len(users)}")

# ========================================================================================
print("\nCOMBINE OPTIONS")
users = (
    session.query(User).filter(
        or_(
            not_(User.name == "Iron Man"),
            and_(
                User.age > 35,
                User.age < 60)
            )
    )
)

for user in users.all():
    print(f'{user.age} - {user.name}')
