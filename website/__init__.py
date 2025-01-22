from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NSJ/8shj4HD.f37h~jjk8#b7' #encrypts cookies and session data.

    return app

