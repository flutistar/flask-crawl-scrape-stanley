# # from app import db, Stadium
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# import os

# app = Flask(__name__)# Generic key for dev purposes only
# app.config.update(
#     SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@localhost:5432/catalog_db',
#     SQLALCHEMY_TRACK_MODIFICATIONS=False
# )
# db = SQLAlchemy(app)
# def inputdata():
#     stadium1 = Stadium(6, 'Levi\'s Stadium', '49ers')
#     stadium2 = Stadium(7, 'AT&T ssPark', 'Giants')
#     stadium3 = Stadium(8, 'Natsss Park', 'Nationals')

#     db.session.add_all([stadium1, stadium2, stadium3])
#     db.session.commit()
# class Stadium(db.Model):
#     __tablename__ = 'stadium'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), nullable=False)
#     team = db.Column(db.String(80), nullable=False)
#     db.create_all()
#     def __init__(self, id, name, team):
#         self.id = id
#         self.name = name
#         self.team = team

#     def __repr__(self):
#         return self.team