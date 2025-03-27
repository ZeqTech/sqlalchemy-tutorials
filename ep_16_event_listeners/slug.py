# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=_cHSW_ehjtY

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection
import re

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class BlogPost(Base):
    __tablename__ = 'blog_posts'
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Add an event through a decorator
@event.listens_for(BlogPost, 'before_insert')
def generate_slug(mapper: Mapper, connection: Connection, target: BlogPost):
    if target.title:
        slug = re.sub(r'[^\w]+', '-', target.title.lower())
        target.slug = slug


# Add an event through a function call
event.listen(BlogPost, 'before_update', generate_slug)

post = BlogPost(title='Decorators are super cool')
session.add(post)
session.commit()

print(post.slug)

post.title = 'Subscribe to Zeq Tech'
session.commit()
print(post.slug)
