from app import db
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
