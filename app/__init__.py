from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()

def create_app():
    app=Flask(__name__)
    login_manager.init_app(app)
    return app

app = create_app()