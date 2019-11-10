from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, TIMESTAMP, UniqueConstraint, JSON

from configs.connector import BaseModel

from model import Mixin


class GithubRepoModel(BaseModel, Mixin):
    __tablename__ = 'github_repo'
    __table_args__ = (
        UniqueConstraint('user_id', 'repo_id'),
    )
    _id = Column(INTEGER, primary_key=True, autoincrement=True)
    repo_id = Column(VARCHAR(128), index=True, nullable=False)
    user_id = Column(VARCHAR(128), index=True, nullable=False)
    name = Column(VARCHAR(128), index=True, nullable=False)
    url = Column(TEXT, nullable=False)
    description = Column(TEXT)
    major_languages = Column(JSON)
    topics = Column(JSON)
    current_version = Column(VARCHAR(64))
    first_commit_id = Column(VARCHAR(40))
    last_commit_id = Column(VARCHAR(40))
    first_commit_time = Column(TIMESTAMP, index=True)
    last_commit_time = Column(TIMESTAMP, index=True, nullable=False)
    doc_site = Column(TEXT)
    resource = Column(VARCHAR(32))
    stars = Column(INTEGER, index=True)
    contributors = Column(INTEGER, index=True)
    commits = Column(INTEGER, index=True)
    issues = Column(INTEGER, index=True)
    forks = Column(INTEGER, index=True)
    watches = Column(INTEGER, index=True)
    created = Column(TIMESTAMP, index=True, nullable=False)
    updated = Column(TIMESTAMP, index=True, nullable=False)


# class GithubTopicRepoMap(BaseModel, Mixin):
#     __tablename__ = 'github_repo_topic_map'
#     __table_args__ = (
#         UniqueConstraint('repo_id', 'topic_id'),
#     )
#     _id = Column(INTEGER, primary_key=True, autoincrement=True)
#     repo_id = Column(VARCHAR(128), index=True, nullable=False)
#     topic_id = Column(VARCHAR(128), index=True, nullable=False)


# class GithubTopicLanguageMap(BaseModel, Mixin):
#     __tablename__ = 'github_repo_language_map'
#     __table_args__ = (
#         UniqueConstraint('repo_id', 'language'),
#     )
#     _id = Column(INTEGER, primary_key=True, autoincrement=True)
#     repo_id = Column(VARCHAR(128), index=True, nullable=False)
#     language = Column(VARCHAR(128), index=True, nullable=False)


class GithubTopicModel(BaseModel, Mixin):
    __tablename__ = 'github_topic'
    __table_args__ = (
        UniqueConstraint('topic_id'),
    )
    _id = Column(INTEGER, primary_key=True, autoincrement=True)
    topic_id = Column(VARCHAR(128), index=True, nullable=False)
    name = Column(VARCHAR(128), index=True, nullable=False)
    url = Column(TEXT, nullable=False)
    description = Column(TEXT)
    avatar_url = Column(TEXT)
    created = Column(TIMESTAMP, index=True, nullable=False)
    updated = Column(TIMESTAMP, index=True, nullable=False)

