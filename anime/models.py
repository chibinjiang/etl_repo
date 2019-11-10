from sqlalchemy import Column, VARCHAR, INTEGER, TIMESTAMP, TEXT, DATE, UniqueConstraint
from configs.connector import BaseModel, session
from model import Mixin


class AnimeAuthorModel(BaseModel, Mixin):
    __tablename__ = 'anime_author'
    _id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(64), nullable=False, index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get_by_name(cls, name):
        model = session.query(cls).filter(cls.name == name).one_or_none()
        return model


class AnimeAuthorBangumiMapModel(BaseModel, Mixin):
    __tablename__ = 'anime_author_bangumi_map'
    __table_args__ = (
        UniqueConstraint("author_id", "bangumi_id"),
    )
    _id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
    author_id = Column(INTEGER, nullable=False, index=True)
    bangumi_id = Column(INTEGER, nullable=False, index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get_by_author_and_bangumi(cls, author_id, bangumi_id):
        model = session.query(cls).filter(cls.author_id == author_id, cls.bangumi_id == bangumi_id).one_or_none()
        return model


class AnimeBangumiModel(BaseModel, Mixin):
    __tablename__ = 'anime_bangumi'
    _id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
    bangumi_id = Column(VARCHAR(64), index=True, nullable=False)
    name = Column(VARCHAR(64), nullable=False, index=True)
    introduction = Column(TEXT)
    cover = Column(VARCHAR(256))
    rank = Column(INTEGER, index=True)  # 指数
    last_updated = Column(DATE, index=True)
    source_url = Column(VARCHAR(256))
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get_by_bangumi_id(cls, bangumi_id):
        model = session.query(cls).filter(cls.bangumi_id == bangumi_id).one_or_none()
        return model


class AnimeEpisodeModel(BaseModel, Mixin):
    __tablename__ = 'anime_episode'
    _id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
    bangumi_id = Column(INTEGER, index=True)  # 外键
    number = Column(INTEGER, index=True)
    episode_id = Column(VARCHAR(64), nullable=False, index=True)
    title = Column(VARCHAR(256))
    source_url = Column(VARCHAR(256))
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get_by_episode_id(cls, episode_id):
        model = session.query(cls).filter(cls.episode_id == episode_id).one_or_none()
        return model

    @classmethod
    def get_by_all_episodes(cls, bangumi_id):
        return AnimeEpisodeModel.query(AnimeEpisodeModel.bangumi_id == bangumi_id)


class AnimeImageModel(BaseModel, Mixin):
    __tablename__ = 'anime_image'
    _id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
    episode_id = Column(INTEGER, nullable=False, index=True)  # 外键
    number = Column(INTEGER, index=True)
    image = Column(VARCHAR(256))
    source_image = Column(VARCHAR(256))
    source_url = Column(VARCHAR(256))
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)
