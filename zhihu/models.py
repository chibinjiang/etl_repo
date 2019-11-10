from sqlalchemy import Column, VARCHAR, INTEGER, TEXT, JSON, PrimaryKeyConstraint, TIMESTAMP

from configs.connector import BaseModel, session

from model import Mixin


class GenderValue(object):
    male = 0
    female = 1


class BooleanValue(object):
    true = 1
    false = 0


class ZhihuTopicModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_topics'

    topic_id = Column(INTEGER, primary_key=True, index=True)
    topic_name = Column(VARCHAR(128), nullable=False, index=True)
    questions_count = Column(INTEGER, nullable=True, index=True)
    followers_count = Column(INTEGER, nullable=True, index=True)
    unanswered_count = Column(INTEGER, index=True, nullable=True)
    best_answerers_count = Column(INTEGER, index=True, nullable=True)
    father_count = Column(INTEGER, index=True, nullable=True)
    best_answers_count = Column(INTEGER, index=True, nullable=True)
    avatar_url = Column(TEXT, nullable=True)  # thumbnail
    category = Column(VARCHAR(16), nullable=True)
    description = Column(TEXT, nullable=True)
    topic_url = Column(VARCHAR(256), nullable=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get(cls, topic_id):
        model = session.query(cls).filter(cls.topic_id == topic_id).one_or_none()
        return model


class ZhihuTopicMapModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_topics_map'
    __table_args__ = (
        PrimaryKeyConstraint('topic_id', 'parent_id'),
    )

    topic_id = Column(INTEGER, nullable=False, index=True)
    parent_id = Column(INTEGER, nullable=False, index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)


class ZhihuQuestionModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_question'

    question_id = Column(INTEGER, primary_key=True, index=True)
    title = Column(VARCHAR(256), nullable=False, index=True)
    user_id = Column(INTEGER, index=True)  # 作者
    is_normal = Column(INTEGER)
    answer_count = Column(INTEGER, index=True)
    visit_count = Column(INTEGER, index=True)
    comment_count = Column(INTEGER, index=True)
    follower_count = Column(INTEGER, index=True)
    collapsed_answer_count = Column(INTEGER, index=True)
    question_type = Column(VARCHAR(16))
    description = Column(TEXT, nullable=True)
    question_url = Column(VARCHAR(256), nullable=True, index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get(cls, question_id):
        model = session.query(cls).filter(cls.question_id == question_id).one_or_none()
        return model


class ZhihuUserModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_user'

    user_id = Column(VARCHAR(32), primary_key=True, index=True)
    name = Column(VARCHAR(128), index=True, nullable=False)
    user_url = Column(VARCHAR(128), index=True)
    user_type = Column(VARCHAR(16))
    gender = Column(INTEGER, index=True)
    identity = Column(VARCHAR(64), index=True)  # 认证
    avatar_url = Column(VARCHAR(128))
    is_org = Column(INTEGER)
    is_advertiser = Column(INTEGER)
    edu_member_tag = Column(JSON)
    master_area = Column(VARCHAR(64))
    subject = Column(VARCHAR(64))
    headline = Column(TEXT)
    url_token = Column(VARCHAR(128), index=True)
    created = Column(TIMESTAMP, nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    @classmethod
    def get(cls, user_id):
        model = session.query(cls).filter(cls.user_id == user_id).one_or_none()
        return model


class ZhihuTopicBestAnswererMapModel(Mixin, BaseModel):
    """
    多对多关系
    """
    __tablename__ = 'zhihu_topic_answer_map'
    __table_args__ = (PrimaryKeyConstraint('topic_id', 'user_id'), )

    topic_id = Column(INTEGER, index=True, nullable=False)
    user_id = Column(VARCHAR(32), index=True, nullable=False)
    created = Column(TIMESTAMP, nullable=False, index=True)


class ZhihuAnswerModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_answer'
    answer_id = Column(INTEGER, primary_key=True, index=True)
    question_id = Column(INTEGER, nullable=False, index=True)
    user_id = Column(INTEGER, nullable=False, index=True)
    is_labeled = Column(INTEGER)
    answer_url = Column(VARCHAR(128), index=True)
    content = Column(TEXT)
    thumbnail = Column(VARCHAR(128))
    comment_count = Column(INTEGER, index=True)
    voteup_count = Column(INTEGER, index=True)
    created_time = Column(TIMESTAMP, index=True, nullable=False)
    updated_time = Column(TIMESTAMP, index=True, nullable=False)
    created = Column(TIMESTAMP, index=True, nullable=False)
    updated = Column(TIMESTAMP, index=True, nullable=False)

    @classmethod
    def get(cls, answer_id):
        model = session.query(cls).filter(cls.answer_id == answer_id).one_or_none()
        return model


class ZhihuArticleModel(Mixin, BaseModel):
    __tablename__ = 'zhihu_article'

    article_id = Column(INTEGER, primary_key=True, index=True)
    title = Column(VARCHAR(256), index=True, nullable=False)
    user_id = Column(INTEGER, index=True, nullable=False)
    content = Column(TEXT)
    voteup_count = Column(INTEGER, index=True)
    comment_count = Column(INTEGER, index=True)
    article_url = Column(VARCHAR(128), index=True, nullable=False)
    image_url = Column(VARCHAR(128))
    topic_thumbnails = Column(JSON)
    created_time = Column(TIMESTAMP, index=True, nullable=False)
    updated_time = Column(TIMESTAMP, index=True, nullable=False)

    @classmethod
    def get(cls, article_id):
        model = session.query(cls).filter(cls.article_id == article_id).one_or_none()
        return model
