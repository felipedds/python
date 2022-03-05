from flask import Flask

import views

def create_app():
    # Main factory
    app = Flask(__name__)
    views.init_app(app)
    return app