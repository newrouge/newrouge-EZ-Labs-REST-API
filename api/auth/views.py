from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import  create_access_token, create_refresh_token
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import jwt_required

auth_namespace = Namespace('auth', description='Authentication')

signup_model=auth_namespace.model(
    'SignUp',{
        'id': fields.Integer(),
        'username':fields.String(required=True,description="Unique username"),
        'email':fields.String(required=True),
        'password':fields.String(required=True,description="make it strong"),

    }
)


user_model= auth_namespace.model(
    'User',{
        'id': fields.Integer(),
        'username':fields.String(required=True,description="Unique username"),
        'email':fields.String(required=True),
        'password_hash':fields.String(required=True,description="make it strong"),
        'email_verified' : fields.Boolean(description = "Email need to be verified"),
        'is_admin': fields.Boolean(description="Admin privileges granted or not")


    }
)

login_model=auth_namespace.model(
    'Login',{
        'email': fields.String(reuired=True),
        'password': fields.String(required=True)
    }
)


@auth_namespace.route("/signup")
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description="Register a new user")
    def post(self):
        """
            User registration
        """

        data=request.get_json()

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED

@auth_namespace.route("/login")
class Login(Resource):

    @auth_namespace.expect(login_model)
    @auth_namespace.doc(description="Sign-in using email & password")
    def post(self):
        """
            User Sign-in
        """
        data = request.get_json()
        email = data.get('email')
        password=data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user) and check_password_hash(user.password,password):
            if user.is_disabled:
                return "User is disabled please contact admin", HTTPStatus.FORBIDDEN
            else:
                access_token= create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)

                response={
                    'access_token':access_token,
                    'refresh_token': refresh_token
                }

                return response, HTTPStatus.OK

        raise BadRequest("Invalid Username or Password")



@auth_namespace.route("/logout")
class Logout(Resource):

    @jwt_required()
    @auth_namespace.doc(description="Revoke Current session")
    def delete(self):
        """
            Logout User session
        """
        pass


