from app import db
import time

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship("Post", backref = 'author', lazy='dynamic')
    password = db.Column(db.String(30))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

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

    def __init__(self, title, url):
        self.title = title
        self.timestamp = time.time()
        self.verified = False
        self.urls = url
    
    def verification(verifier_id, false_news_status):
        self.user_id = verified_id
        self.verified = True
        self.false_news = false_news_status

    
