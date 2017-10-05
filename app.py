'''

Handling the general imports

'''


from flask import Flask, render_template, request
from forms import *


'''

Application Configuration

'''

app = Flask(__name__)
app.config.from_object('config')

'''

Controller - Handling the routes.

'''

@app.route('/', methods=['GET'])
def home():
    return "Home"


@app.errorhandler(404)
def error404():
    return render_template("error/404.html"), 404

'''

Handling the launch of application

'''
if __name__ == '__main__':
    app.run()