from ..utils import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.Text(),nullable=False)
    email_verified = db.Column(db.Boolean(),default=False)
    is_admin=db.Column(db.Boolean(),default=False)
    is_disabled=db.Column(db.Boolean(),default=False)

    def __repr__(self):
        return f"<User {self.username}>"


    def save(self):
        db.session.add(self)
        db.session.commit()