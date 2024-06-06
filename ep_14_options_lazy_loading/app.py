# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=2fwdjkL0jqw

from sqlalchemy import select
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    lazyload,
    load_only,
    noload,
    raiseload,
)

from models import Detail, Post, User, session

# Loading Options:

# Lazy Loading (Loaded maybe when accessed)
# noload()          - doesn't load the data at all
# lazyload()        - will load the data only when accessed
# raiseload()       - doesn't load the data - will raise an error if the data is accessed

# Special:
# load_only()       - only load specific columns

# =============================================================================================
# Lazy Loading

print('=' * 40)
print('\nLoading with the: `noload` function')
query = session.query(User).options(noload(User.posts))
print(query)
print(query.all())


print('=' * 40)
print('\nLoading with the: `lazyload` function')
query = session.query(User).options(lazyload(User.posts))
print(query)
print(query.all())


print('=' * 40)
print('\nLoading with the: `raiseload` function')
query = session.query(User).options(raiseload(User.posts))
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

# =============================================================================================
# load_only()
print('=' * 40)
print('\nUsing the: `load_only` function in options')
print('\nApply `load_only()` to only load selected columns')
query = select(User).options(joinedload(User.posts).options(load_only(Post.active)))
print(query)

# Need to add unique when adding a joinedload or
# contains_eager when using `select()`
print(session.scalars(query).unique().all())

# =============================================================================================
# Multiple Loading

print('=' * 40)
print('\nJoin load the posts, lazily load the preferences')
query = (
    session.query(User)
    .options(
        joinedload(User.posts),
        lazyload(User.preference)
    )
)
print(query)
print(query.all())

# =============================================================================================
# Chained Loading

print('=' * 40)
print('\nApply CHained loading')
query = (
    session.query(User)
    .options(
        joinedload(User.posts)
        .lazyload(Post.detail)
    )
)
print(query)
print(query.all())
