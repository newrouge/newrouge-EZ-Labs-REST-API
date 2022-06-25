from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from ..models.user import User
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.exceptions import Forbidden, Unauthorized, NotAcceptable
from decouple import config
from ..utils import mail
from ..utils import db

s = URLSafeTimedSerializer(config('SECRET_KEY'))

client_namespace=Namespace('client', description='Client Interaction')

user_model= client_namespace.model(
    'User',{
        'username':fields.String(required=True,description="Unique username"),
        'email':fields.String(required=True),
        'is_admin': fields.Boolean(description="Admin privileges granted or not"),
        'email_verified' : fields.Boolean(description="Email need to be verified"),
          }
)

@client_namespace.route("/profile")
class GetProfile(Resource):

    @jwt_required()
    @client_namespace.doc(description="Request your profile data")
    @client_namespace.marshal_with(user_model)
    def get(self):
        """
            Fetch profile data.
        """
        current_user= get_jwt_identity()
        user=User.query.filter_by(username=current_user).first()
        return user, HTTPStatus.OK




@client_namespace.route("/verify/<string:username>")
class InitiateVerification(Resource):

    @jwt_required()
    @client_namespace.doc(description="Issue Verify Email Address")
    def get(self,username):
        """
            Issue user email verification token
        """

        current_user= get_jwt_identity()
        tuser=User.query.filter_by(username=username).first()

        if tuser is not None:
            if current_user != tuser.username:
                raise Unauthorized("Not Authorized")
            else:
                temail = tuser.email


                token = s.dumps(temail, salt=config('salt'))

                message='Verify your email at http://localhost:5000/clients/confirm_email/{} '.format(token)

                mail.send_mail(message,temail)

                return 'Verify your email at http://localhost:5000/clients/confirm_email/{} '.format(token)


        raise NotAcceptable("Wrong Username")


@client_namespace.route("/confirm_email/<string:token>")
class VerifyUser(Resource):

    @jwt_required()
    def get(self,token):
        try:
            email = s.loads(token, salt=config('salt'), max_age=3600)

            current_user=get_jwt_identity()
            tuser=User.query.filter_by(email=email).first()

            if tuser.username != current_user:
                raise Unauthorized("Not Authorized")
            else:
                user = User.query.filter_by(email=email).first()
                user.email_verified=1
                db.session.commit()

                return "<h1> Email Verified!</h1>", HTTPStatus.OK

        except SignatureExpired:
            return '<h1>The token is expired!</h1>', HTTPStatus.BAD_REQUEST

