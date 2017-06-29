#-*- coding:utf-8 -*-
_author__ = 'ZHANGJUN'

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ForumPost(Base):
    __tablename__ = 'forum_posts'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(50), unique=False)
    post_title = Column(String(50), unique=False)
    post_user_id = Column(String(50), ForeignKey('users.user_id'), index=True, nullable=False)
    post_detail_href = Column(String(150), nullable=False)
    post_user_nick = Column(String(50), unique=False)
    post_user_href = Column(String(150), unique=False)
    post_detail_href_children = Column(String(250), nullable=False)
    post_publish_time = Column(String(150), unique=False)

    def __init__(self, post_id, post_title, post_user_id, post_detail_href, post_user_nick,
                    post_user_href, post_detail_href_children=None, post_publish_time=None):
        self.post_id = post_id
        self.post_title = post_title
        self.post_user_id = post_user_id
        self.post_detail_href = post_detail_href
        self.post_user_nick = post_user_nick
        self.post_user_href = post_user_href
        self.post_detail_href_children = post_detail_href_children
        self.post_publish_time = post_publish_time


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True)
    user_nick = Column(String(50), unique=False)
    user_name = Column(String(50), unique=False)
    user_sex = Column(String(50), unique=False)
    user_weibo = Column(String(50), unique=False)
    user_qq = Column(String(50), unique=False)
    user_sign = Column(String(250), unique=False)
    user_address = Column(String(100), unique=False)
    user_reg_time = Column(String(100), unique=False)

    def __init__(self, user_id, user_nick=None, user_name=None, user_sex=None, user_weibo=None,
                 user_qq=None, user_sign=None, user_address=None, user_reg_time=None):
        self.user_id = user_id
        self.user_nick = user_nick
        self.user_name = user_name
        self.user_sex = user_sex
        self.user_weibo = user_weibo
        self.user_qq = user_qq
        self.user_sign = user_sign
        self.user_address = user_address
        self.user_reg_time = user_reg_time


class ForumPostDetail(Base):
    __tablename__ = 'forum_posts_lc'
    id = Column(Integer, primary_key=True)
    post_id = Column(String(50), ForeignKey('forum_posts.post_id'), index=True, nullable=False)
    post_lc_num = Column(Integer)
    post_lc_time = Column(String(50), unique=False)
    post_lc_user_id = Column(String(50), ForeignKey('users.user_id'), index=True, nullable=False)
    post_lc_user_nick = Column(String(50), unique=False)
    post_lc_title = Column(String(50), unique=False)
    post_lc_img_info = Column(String(250), unique=False)
    post_lc_img_url = Column(String(50), unique=False)
    post_lc_img_path = Column(String(150), unique=False)

    def __init__(self, post_id, post_lc_num, post_lc_user_id, post_lc_time=None, post_lc_user_nick=None, post_lc_title=None,
                 post_lc_img_info=None, post_lc_img_url=None, post_lc_img_path=None):
        self.post_id = post_id
        self.post_lc_num = post_lc_num
        self.post_lc_user_id = post_lc_user_id
        self.post_lc_time = post_lc_time
        self.post_lc_user_nick = post_lc_user_nick
        self.post_lc_title = post_lc_title
        self.post_lc_img_info = post_lc_img_info
        self.post_lc_img_url = post_lc_img_url
        self.post_lc_img_path = post_lc_img_path