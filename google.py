import os

import requests
from flask import Flask, redirect, url_for, json, flash, render_template
from flask_dance.contrib.google import make_google_blueprint, google

from app.forms import FinderForm

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint(scope=["profile", "email"])
app.register_blueprint(google_bp, url_prefix="/login")

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text

    form = FinderForm()

    try:
        link = 'https://ancient-springs-63198.herokuapp.com/api/books'
        res = requests.get(link)
    except:
        return False

    json_list = json.loads(res.text)
    print(json_list)

    if form.validate_on_submit():
        flash('ID requested for ID {}'.format(form.username.data))
        print('Searching for book number ' + form.username.data)

        return redirect(url_for('json_example', keys=form.username.data))

    # jsonfile type = list
    return render_template('index.html', jsonfile=Stats(json_list), email=resp.json()["email"], title='Sign In', form=form)

    return "You are {email} on Google".format(email=resp.json()["email"])

@app.route("/json_example/<keys>", methods=['GET','POST'])
def json_example(keys):
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text

    form = FinderForm()

    try:
        link = 'https://ancient-springs-63198.herokuapp.com/api/books'
        link_edited = link + '/' + keys
        res = requests.get(link_edited)

        json_dictionary = json.loads(res.text)
        print(json_dictionary)
    except:
        return False

    if form.validate_on_submit():
        flash('ID requested for ID {}'.format(form.username.data))
        print('Searching for book number ' + form.username.data)
        return redirect(url_for('json_example', keys=form.username.data))

    # jsonfile type = dict
    return render_template('index2.html', jsonfile=json_dictionary, email=resp.json()["email"], title='Sign In', form=form)


# test run
if __name__ == '__main__':
    app.run()


# to convert json_list into dictionaries
class Stat:
    def __init__(self, stat):
        print(type(stat))
        print(stat)
        self.__dict__ = {a:Stat(b) if isinstance(b, dict) else b for a, b in stat.items()}


class Stats:
   def __init__(self, full_data):
      self.full_data = full_data
   def __iter__(self):
      for i in self.full_data:
         yield Stat(i)