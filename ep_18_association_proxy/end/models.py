# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=jmjuaSVRWPY

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class UserArticle(Base):
    __tablename__ = 'user_article'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    article_id: Mapped[int] = mapped_column(ForeignKey('article.id'))


class User(Base):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String(50))
    articles: Mapped[list['Article']] = relationship(
        back_populates='users', secondary='user_article'
    )

    # This was added
    # Association proxy: jump straight to article titles
    article_titles: Mapped[list[str]] = association_proxy('articles', 'title')


class Article(Base):
    __tablename__ = 'article'

    title: Mapped[str] = mapped_column(String(100))
    users: Mapped[list[User]] = relationship(
        back_populates='articles', secondary='user_article'
    )

    # This was added
    # Association proxy: jump straight to user names
    users_name: Mapped[list[str]] = association_proxy('users', 'name')
