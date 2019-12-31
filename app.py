# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
from crawel import getLinks, getOrgName
import re
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrap import startscrap


app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
app.config.update(
    # SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@localhost:5432/catalog_db',
    SQLALCHEMY_DATABASE_URI='postgres://ohayvqyxnddnxu:09cfa7da423988d4c477dd363254cb422fbcb04074f02c3cbf74c5af3ca4e441@ec2-174-129-33-196.compute-1.amazonaws.com:5432/d4u780p859e9eg',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)

# Heroku
from flask_heroku import Heroku
heroku = Heroku(app)


def get_session():
    return sessionmaker(bind=create_engine('postgresql://postgres:password@localhost:5432/catalog_db'))()


def get_user():
    username = session['username']
    user = db.session.query(User).filter(User.username.in_([username])).first()
    return user


def add_user(username, password, email):
    u = User(username=username, password=password.decode('utf8'), email=email)
    db.session.add(u)
    db.session.commit()


def change_user(**kwargs):
    username = session['username']
    user = db.session.query(User).filter(User.username.in_([username])).first()
    for arg, val in kwargs.items():
        if val != "":
            setattr(user, arg, val)
    db.session.commit()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
        user = db.session.query(User).filter(User.username.in_([username])).first()
        # user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False


def username_taken(username):
    user = db.session.query(User).filter(User.username.in_([username])).first()
    return user

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = get_user()
    return render_template('home.html', user=user)

# --------- Log out ------------------------------------------------------------- #
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# ---------Open SignUp ---------------------------------------------------------- #

@app.route("/gosignup")
def gosignup():
    # session['logged_in'] = False
    return render_template('signup.html')

# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if not session.get('logged_in'):
    form = forms.LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = hash_password(request.form['password'])
        email = request.form['email']
        if form.validate():
            if not username_taken(username):
                add_user(username, password, email)
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('login'))
            return json.dumps({'status': 'Username taken'})
        return json.dumps({'status': 'User/Pass required'})
    return render_template('login.html', form=form)
    # return redirect(url_for('logout'))

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = hash_password(password)
            email = request.form['email']
            change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# --------- Input Url ------------------------------------------------------------- #
@app.route("/input_url", methods=['GET', 'POST'])
def input_url():
    if request.method == 'POST':
        url = request.values['inputurl']
        url = url.strip()
        if url == '':
            return json.dumps({'links': 'Blank url'})
        # Crawl with given url
        rst_links = []
        try:
            rst_links= getLinks(url)
        except:
            print('Empty Crawled results', url)
        # results = db.session.query(CrawledLinks.url).all()
        # print(type(rst_links))
        if type(rst_links) is not str:
            # org_results = db.session.query(OriginalUrl.url).all()
            # org_urls = helpers.getorgdata(url)
            # print(len(org_results))
            org_urls = []
            rst = OriginalUrl.query.all()
            if len(rst) != 0:
                org_urls = [row.url for row in rst]
                # org_urls = list(rst)
                print(type(org_urls))
            if not url in org_urls:
                # helpers.addorgdata(url)
                entry = OriginalUrl(url = url)
                db.session.add(entry)
                db.session.commit()
                # org_id = helpers.getorgnum()
                org_id = len(org_urls)
                # orgname = getOrgName(url)
                # print(orgname)
                org_sub_num = 1
                for item in rst_links:
                    # if not item[1] in result_list:
                    orgid = str(org_id) + '-' + str(org_sub_num)
                    # helpers.addcrawldata(orgid, url, item[0], item[1])
                    entry = CrawledLinks(orgid = orgid, originalurl = url, pagetitle = item[0], url = item[1])
                    db.session.add(entry)
                    db.session.commit()
                    org_sub_num += 1 
                # org_add_row = OriginalUrl(id = org_id, url = url)
                # db.session.add(org_add_row)
                # db.session.commit()
            else:
                # org_id = len(org_urls)
                print('Duplicated')
            
            
    return json.dumps({'links': rst_links})

# --------- Scrap page ------------------------------------------------------------- #
@app.route("/scrap", methods=['GET', 'POST'])
def scrap_page():
    # if session.get('logged_in'):
    if request.method == 'GET':
        # with helpers.session_scope() as s:
            # data = s.query(tabledef.CrawledLinks).all()
        data = CrawledLinks.query.all()
        return render_template('scrap.html', data = data)
    return json.dumps({'status': 'Failed'})
    # return redirect(url_for('login'))

@app.route("/viewscraped", methods=['GET', 'POST'])
def view_data():
    # if session.get('logged_in'):
    if request.method == 'GET':
        data = ScrapedData.query.all()
        return render_template('viewdata.html', data = data)
    return json.dumps({'status': 'Failed'})
    # return redirect(url_for('login'))
# @app.route("/viewscraped", methods=['GET', 'POST'])
# def view_data():
#     if session.get('logged_in'):
#         if request.method == 'GET':
#             with helpers.session_scope() as s:
#                 # data = tabledef.ScrapedData.query.all()
#                 data = s.query(tabledef.ScrapedData).all()
#             return render_template('viewdata.html', data = data)
#         return json.dumps({'status': 'Failed'})
#     return redirect(url_for('login'))
# --------- Run Scraper ------------------------------------------------------------- #
@app.route("/startscrape", methods=['GET', 'POST'])
def startscrape():
    if request.method == 'POST':
        url = request.values['scrapurl']
        data = startscrap(url)
        if type(data) is not str:
            entry = ScrapedData(url = url, title = data[0], keywords ='keys', content = data[1])
            db.session.add(entry)
            db.session.commit()
            return json.dumps({'title': data[0]})
        # results = db.session.query(CrawledLinks.url).all()
        # result_list = [row[0] for row in results]
        # for url in result_list:
        #     data = startscrap(url)
        #     if data != 'Scrap Failed':
        #         print('Scraped url', url)
                
            
        else:
            return json.dumps({'title': 'failed'})
    return json.dumps({'status': 'Failed'})
# @app.route("/startscrape", methods=['GET', 'POST'])
# def startscrape():
#     if request.method == 'POST':
#         url = request.values['scrapurl']
#         data = startscrap(url)
#         if type(data) is not str:
#             with helpers.session_scope() as s:
#                 entry = tabledef.ScrapedData(url = url, title = data[0], keywords ='keys', content = data[1])
#                 s.add(entry)
#                 s.commit()
#             return json.dumps({'title': data[0]})
#         # results = db.session.query(CrawledLinks.url).all()
#         # result_list = [row[0] for row in results]
#         # for url in result_list:
#         #     data = startscrap(url)
#         #     if data != 'Scrap Failed':
#         #         print('Scraped url', url)
                
            
#         else:
#             return json.dumps({'title': 'failed'})
#     return json.dumps({'status': 'Failed'})
# ======== Data Schema ============================================================== #
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(512))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '<User %r>' % self.username
class OriginalUrl(db.Model):
    __tablename__ = 'originalurls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(250), nullable=False)
    
    def __init__(self, url):
        self.url = url
        # self.id = id

    def __repr__(self):
        return self.url
class CrawledLinks(db.Model):
    __tablename__ = 'crawledlinks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orgid = db.Column(db.String(20), nullable = False)
    originalurl = db.Column(db.String(250), nullable=False)
    pagetitle = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def __init__(self, orgid, originalurl, pagetitle, url):
        self.orgid = orgid
        self.originalurl = originalurl
        self.pagetitle = pagetitle
        self.url = url

    def __repr__(self):
        return self.url
class ScrapedData(db.Model):
    __tablename__ = 'scrapeddata'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    keywords = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, url, title, keywords, content):
        self.url = url
        self.title = title
        self.keywords = keywords
        self.content = content

    def __repr__(self):
        return self.url
# ======== Main ============================================================== #
if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(debug=False, use_reloader=True, host="0.0.0.0")
