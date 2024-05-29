from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

db_url = 'sqlite:///ep_13_options_eager_loading.db'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    posts: Mapped[list['Post']] = relationship(
        backref='user',
        lazy='select',
    )

    def __repr__(self):
        return f'<User {self.name} >'


class Post(Base):
    __tablename__ = 'posts'
    active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    detail: Mapped['Detail'] = relationship(backref='post', lazy='select')

    @classmethod
    def is_active(cls):
        return cls.active is True

    def __repr__(self):
        return f'<Post {self.id} >'


class Detail(Base):
    __tablename__ = 'details'
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Detail {self.id} - content: {self.content}>'


# Create the database tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    user_1 = User(name='Zeq')
    user_1.posts = [
        Post(detail=Detail(content='This is an example post detail')),
        Post(detail=Detail(content='Subscribe to Zeq Tech!'), active=True),
    ]

    user_2 = User(name='Bill')
    user_2.posts = [
        Post(detail=Detail(content='This is another example of some post details')),
        Post(detail=Detail(content='Yes!')),
    ]

    session.add_all([user_1, user_2])
    session.commit()
