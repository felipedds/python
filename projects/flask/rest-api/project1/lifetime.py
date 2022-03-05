# Lifetime of Flask
from flask import Flask

app = Flask(__name__)

# Contexts
## 1 - Configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DB_URI'] = 'mysql://..'

# Add routes
@app.route('/index')
def index():
    ...
app.add_url_rule('path', ...)

# Initialize extension
from flask_admin import Admin

# Register blueprints
app.register_blueprints(...)

# Add hooks
@app.before_request(...)
@app.error_handler(...)

# Call other factories
views.init_app(app)

## 2 - Application
# Globals FLask's object (request, session, g)
app.test_client
debug

## 3 - Request Context
from flask import request, session, g
request.args
request.form

