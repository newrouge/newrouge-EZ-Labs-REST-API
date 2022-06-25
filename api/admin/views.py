from flask_restx import Resource, Namespace, fields
from ..models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from flask import request
from ..utils import db
from werkzeug.exceptions import Forbidden, Unauthorized

admin_namespace = Namespace('admin', description='Require Admin privileges')

access_model=admin_namespace.model(
    'accesscontrol',{
        'username':fields.String(required=True),
        'is_disabled':fields.Boolean(required=True),

    }
)

user_model= admin_namespace.model(
    'User',{
        'id': fields.Integer(),
        'username':fields.String(required=True,description="Unique username"),
        'email':fields.String(required=True),
        'email_verified' : fields.Boolean(description = "Email need to be verified"),
        'is_admin': fields.Boolean(description="Admin privileges granted or not")


    }
)

@admin_namespace.route("/listusers")
class GetClientsList(Resource):

    @jwt_required()
    @admin_namespace.marshal_with(user_model)
    @admin_namespace.doc(description="List all user's data")
    def get(self):
        """
            Admin Listing all clients
        """
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if user.is_admin:

            users= User.query.all()

            return users, HTTPStatus.OK

        raise Forbidden("Only admin can list users")


@admin_namespace.route("/profile/access")
class ChangeUserAccess(Resource):

    @jwt_required()
    @admin_namespace.expect(access_model)
    @admin_namespace.doc(description="Enable or Disable a user from login. ")
    def post(self):
        """
            Disable/Enable a User
        """
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if user.is_admin == 0:
            return "Only admin can disable a User", HTTPStatus.FORBIDDEN
        else:
            data = request.get_json()
            username=data.get('username')
            is_disabled=data.get('is_disabled')

            target_user=User.query.filter_by(username=username).first()
            target_user.is_disabled=is_disabled
            db.session.commit()


            return {"username" : username,"is_disabled":is_disabled}, HTTPStatus.OK

@admin_namespace.route("/profile/<string:username>")
class GetSingleUser(Resource):

    @jwt_required()
    @admin_namespace.marshal_with(user_model)
    @admin_namespace.doc(description="Fetching a particular profile data")
    def get(self,username):
        """
            View a single profile
        """
        current_user= get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if user.is_admin:

            tuser = User.query.filter_by(username=username).first()

            return tuser, HTTPStatus.OK

        elif current_user == username:
            tuser = User.query.filter_by(username=username).first()

            return tuser, HTTPStatus.OK

        raise Unauthorized("You are not authorized to view this")


