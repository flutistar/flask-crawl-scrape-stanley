# -*- coding: utf-8 -*-

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Local
SQLALCHEMY_DATABASE_URI = 'sqlite:///accounts.db'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/catalog_db'

# Heroku
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# SQLALCHEMY_DATABASE_URI = os.environ['postgres://ohayvqyxnddnxu:09cfa7da423988d4c477dd363254cb422fbcb04074f02c3cbf74c5af3ca4e441@ec2-174-129-33-196.compute-1.amazonaws.com:5432/d4u780p859e9eg']

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(512))
    email = Column(String(50))

    def __repr__(self):
        return '<User %r>' % self.username
# class ScrapedData(Base):
#     __tablename__ = 'scrapeddata'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     url = Column(String(250), nullable=False)
#     title = Column(String(80), nullable=False)
#     keywords = Column(String(80), nullable=False)
#     content = Column(Text, nullable=False)

#     # def __init__(self, url, title, keywords, content):
#     #     self.url = url
#     #     self.title = title
#     #     self.keywords = keywords
#     #     self.content = content

#     def __repr__(self):
#         return self.url

# class OriginalUrl(Base):
#     __tablename__ = 'originalurl'
#     id = Column(Integer, primary_key=True, autoincrement = True)
#     # orgname = Column(String(120), nullable=False)
#     url = Column(String(250), nullable=False)
    
#     # def __init__(self, url, id):
#     #     self.id = id
#     #     self.url = url

#     def __repr__(self):
#         return self.url
# class CrawledLinks(Base):
#     __tablename__ = 'crawledlinks'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     orgid = Column(String(20), nullable = False)
#     originalurl = Column(String(250), nullable=False)
#     pagetitle = Column(String(80), nullable=False)
#     url = Column(String(250), nullable=False)

#     # def __init__(self, orgid, originalurl, pagetitle, url):
#     #     self.orgid = orgid
#     #     self.originalurl = originalurl
#     #     self.pagetitle = pagetitle
#     #     self.url = url

#     def __repr__(self):
#         return self.orgid

engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
