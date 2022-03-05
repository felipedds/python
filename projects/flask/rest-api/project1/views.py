from flask import Flask, request

def init_app(app: Flask):
    # Initialization of extensions
    @app.route('/')
    def index():
        print(request.args)
        return 'Index'
    
    @app.route('/contact')
    def contact():
        print(request.args)
        return 'Contact'