from flask import Flask
from flask_login import LoginManager
from auth.auth_views import auth
from operation.operation_views import operation
from reports_and_download.reports_and_download import reports_and_download
from models import *
from flask_dance.contrib.github import make_github_blueprint


import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'notmuchsecreat'


db.init_app(app)

github_blueprint = make_github_blueprint(client_id=os.environ.get('client_id'),client_secret=os.environ.get('client_secret'))
app.register_blueprint(github_blueprint,url_prefix="/github_login")

app.register_blueprint(auth)
app.register_blueprint(operation)
app.register_blueprint(reports_and_download)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

'''
if __name__ == '__main__':
 
    app.run()
'''