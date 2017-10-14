'''

Handling the general imports

'''


from flask import Flask, render_template, request, render_template, flash, redirect, session, url_for, request, g
from forms import *
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import dirCurrent
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from reuters import reutersTitles
from semantic import *
'''

Application Configuration

'''

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(dirCurrent, 'tmp'))
import time

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)


    def __repr__(self):
        return '<User %r>' % (self.username)

    def parse_json(self):
        return '{"id" : %r, "username":%r, "password":%r}' % (self.id, self.username, self.password)

    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=time.time())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    urls = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=0)
    false_news = db.Column(db.Boolean)

    def __repr__(self):
        return '<Post %r>' % (self.id)

class UserView(ModelView):
        can_delete = True  # disable model deletion
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True

class PostView(ModelView):
        page_size = 50  # the number of entries to display on the list view


'''

Controller - Handling the routes.

'''




@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        search = request.form.search.data
        maximum = -199
        titles = reutersTitles()
        index = 0
        for title in titles:
            value = similarity(title, search, True)
            if (value > maximum):
                maximum = value
                index = title
        value = sentimentAnalysis(title, search)
        if value:
            return 
        else:



    form = SearchForm(request.form)
    return render_template("home.html", form=form )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        if form.validate:
            username = form.username
            password = form.password
            email = form.email
            user = User(username, password, email)
            user.parse_json()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('home')
        

@app.errorhandler(404)
def error404(error):
    return render_template("error/404.html"), 404

'''

Handling the launch of application

'''
admin = Admin(app, name='Admin')
admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)