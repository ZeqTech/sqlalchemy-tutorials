# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================

from sqlalchemy import select
from sqlalchemy.orm import (
    contains_eager,
    defaultload,
    immediateload,
    joinedload,
    load_only,
    selectinload,
    subqueryload,
)

from models import Detail, Post, User, session


# Loading Options:
# defaultload()         - when you dont want to change the loading behavior but you
#                         want to change something in the loaded items from the relationship

# Eager loading: (Loaded right away)
# joinedload()          - load related data with a join statement
# subqueryload()        - loads data using a subquery
# immediateload()       - loads everything in the relationship one by one, can add a recursion depth for self relationships
#                         ex: followers / following relationships
# selectinload()        - more efficient than `immediateload`,` creating one select statment for all related objects

# Special:
# contains_eager()  - allows filtering on related items

# =============================================================================================
# Default Loading
print('=' * 40)
print('\nLoading from class structure')
query = session.query(User)
print(query)

print('=' * 40)
print('\nLoading with the: `defaultload` function')
query = session.query(User).options(defaultload(User.posts))
print(query)

# =============================================================================================
# Eager Loading

print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = session.query(User).options(joinedload(User.posts)).all()
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `subqueryload` function')
query = session.query(User).options(subqueryload(User.posts))
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `immediateload` function')
query = session.query(User).options(immediateload(User.posts))
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `selectinload` function')
query = session.query(User).options(selectinload(User.posts))
print(query)
print(query.all())

# =============================================================================================
# Select use of joinedload and contains_eager
print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = (
    select(User).options(joinedload(User.posts)).filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(session.execute(query).unique().all())

print('=' * 40)
print('\nLoading with the: `contains_eager` function')
query = (
    select(User)
    .outerjoin(Post)
    .options(contains_eager(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(session.execute(query).unique().all())

# Query use of joinedload and contains_eager
print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = (
    session.query(User)
    .options(joinedload(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(query.all())

# contains eager requires us to specify a join condition,
# but also allows us to filter onthe joined data
print('=' * 40)
print('\nLoading with the: `contains_eager` function')
query = (
    session.query(User)
    .outerjoin(Post)
    .options(contains_eager(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(query.all())

# =============================================================================================
# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nMore `.options()` loading')
print('\nApply `load_only()` to only load selected columns')
query = (
    session.query(User)
    .outerjoin(Post)
    .options(
        contains_eager(User.posts).options(joinedload(Post.detail), load_only(Post.id))
    )
)
print(query)

print('=' * 40)
print('\nMore `.options()` loading')
query = session.query(User).options(
    joinedload(User.posts).options(joinedload(Post.detail), load_only(Post.id))
)
print(query)

# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nLoad only the Post id for all Posts for a User')
query = session.query(User).options(joinedload(User.posts).load_only(Post.id))
print(query)

print('=' * 40)
print("\nLoad all Posts for User and only the Detail's content for each post")
query = session.query(User).options(
    joinedload(User.posts).joinedload(Post.detail).load_only(Detail.content)
)
print(query)
