# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================

from typing import Optional

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine('sqlite:///ep_12_joins.db')
session = sessionmaker(bind=engine)()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f'< {self.__class__.__name__} id: {self.id}>'


class Address(Base):
    __tablename__ = 'addresses'

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    data: Mapped[str]


class User(Base):
    __tablename__ = 'users'

    first_name: Mapped[str]
    last_name: Mapped[str]
    address: Mapped[Address] = relationship()


# Create the database tables
Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(User).count() < 1:
    # This address IS used
    address_1 = Address(data='1234 Random Address')

    # These addresses are NOT used
    address_2 = Address(data='5678 Non-existant Address')
    address_3 = Address(data='9012 Extra Address')

    # User with an address
    user_1 = User(
        first_name='Zeq',
        last_name='Tech',
        address=address_1,
    )

    # User without an address
    user_2 = User(
        first_name='Banana',
        last_name='Man',
        address=None,
    )

    session.add_all([address_1, address_2, address_3, user_1, user_2])
    session.commit()

# INNER JOIN
# Return all the users that have addresses
result = session.query(User).join(Address).filter(User.id == Address.user_id).all()
print('\nINNER JOIN')
print(result)

result = (
    session.query(User, Address).join(Address).filter(User.id == Address.user_id).all()
)
print('\nINNER JOIN')
print(result)

# ANTI INNER JOIN - Inverse
# Return all the users that dont have addresses
# and all Addresses that dont have users
result = (
    session.query(User, Address)
    .join(Address, full=True)
    .filter(User.address is None, Address.user_id == None)
    .all()
)
print('\nANTI INNER JOIN - Inverse')
print(result)


# LEFT OUTER JOIN
# Return all users regardless if they have addresses or not
result = (
    session.query(User, Address).outerjoin(Address, User.id == Address.user_id).all()
)
print('\nLEFT OUTER JOIN')
print(result)

# ANTI LEFT OUTER JOIN - Inverse
# Return all users regardless if they have addresses or not
result = (
    session.query(User, Address).outerjoin(Address).filter(User.address == None).all()
)
print('\nANTI LEFT OUTER JOIN - Inverse')
print(result)

# RIGHT OUTER JOIN
# Return all addresses regardless if they have users or not
result = session.query(Address, User).outerjoin(User).all()
print('\nRIGHT OUTER JOIN')
print(result)

# ANTI RIGHT OUTER JOIN - Inverse
# Return all addresses regardless if they have users or not
result = (
    session.query(Address, User).outerjoin(User).filter(Address.user_id == None).all()
)
print('\nANTI RIGHT OUTER JOIN - Inverse')
print(result)

# FULL OUTER JOIN
# SQLAlchemy doesn't support Full Outer Join directly,
# but it can be achieved with UNION
left_join = session.query(User, Address).outerjoin(Address)  # Gets all Users
right_join = session.query(User, Address).outerjoin(User)  # Gets all Addresses
full_outer_join = left_join.union(right_join)
print('\nFULL JOIN')
print(full_outer_join.all())

# This will return all rows, regardless if there is a user associated with the Address
# or regardless if there is an address associated with a user
result = session.query(User, Address).join(Address, isouter=True, full=True).all()
print('\nFULL JOIN')
print(result)
