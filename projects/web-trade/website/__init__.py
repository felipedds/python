from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import views
    from .routes import routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')
    return app