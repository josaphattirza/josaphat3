from flask import jsonify, render_template, redirect, url_for, flash
from app import app
from app.forms import FinderForm
import requests
import json

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
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
    return render_template('index.html', jsonfile = Stats(json_list), title='Sign In', form=form)


@app.route("/json_example/<keys>", methods=['GET','POST'])
def json_example(keys):
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
    return render_template('index2.html', jsonfile=json_dictionary, title='Sign In', form=form)


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

