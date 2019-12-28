# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
from crawel import getLinks
import re
from flask_sqlalchemy import SQLAlchemy
from model import inputdata
from scrap import startscrap


app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
app.config.update(
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@localhost:5432/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)

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
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
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
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    print('signup success')
                    return render_template('login.html')
                print('username taken')
                return json.dumps({'status': 'Username taken'})
            print('User/Pass required')
            return json.dumps({'status': 'User/Pass required'})
        print('login.html')
        return render_template('login.html', form=form)
    print('login')
    return redirect(url_for('logout'))

# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# --------- Input Url ------------------------------------------------------------- #
@app.route("/input_url", methods=['GET', 'POST'])
def input_url():
    if request.method == 'POST':
        url = request.values
        # Crawl with given url
        rst_links= getLinks(url['inputurl'])
        results = db.session.query(CrawledLinks.url).all()
        result_list = [row[0] for row in results]
        print(type(rst_links))
        if type(rst_links) is not str:
            for item in rst_links:
                if not item[1] in result_list:
                    entry = CrawledLinks(url['inputurl'], pagetitle =item[0], url = item[1])
                    db.session.add(entry)
                    db.session.commit()
    return json.dumps({'links': rst_links})

# --------- Scrap page ------------------------------------------------------------- #
@app.route("/scrap", methods=['GET', 'POST'])
def scrap_page():
    if session.get('logged_in'):
        if request.method == 'GET':
            data = CrawledLinks.query.all()
            return render_template('scrap.html', data = data)
        return json.dumps({'status': 'Failed'})
    return redirect(url_for('login'))

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

# ======== Data Schema ============================================================== #
class CrawledLinks(db.Model):
    __tablename__ = 'crawledlinks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    originalurl = db.Column(db.String(250), nullable=False)
    pagetitle = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def __init__(self, originalurl, pagetitle, url):
        self.originalurl = originalurl
        self.pagetitle = pagetitle
        self.url = url

    def __repr__(self):
        return self.id
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
        return self.id
# ======== Main ============================================================== #
if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
