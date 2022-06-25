from flask import Flask, url_for
from .auth.views import auth_namespace
from .clients.views import client_namespace
from .admin.views import admin_namespace
from flask_restx import Api

from .models.verify import Verify
from .utils import db
from .models.user import User
from flask_migrate import Migrate
from .config.config import config_dict
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    jwt=JWTManager(app)
    # migrate = Migrate(app,db)

    authorizations= {
        "Bearer Auth": {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add JWT access_token e.g  Bearer &lt;TOKEN&gt;'
        }
    }
    api = Api(app,title="EZ LABS API", description="REST API",
              authorizations=authorizations,
              security="Bearer Auth",
              )




    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(client_namespace, path="/clients")
    api.add_namespace(admin_namespace,)



    @api.errorhandler(NotFound)
    def notfound(error):
        return {"Error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"Error":"Method Not Allowed"}, 405

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
        }

    return app
