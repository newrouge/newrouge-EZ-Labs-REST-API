from ..utils import db

class Verify(db.Model):
    __tablename__ = "verify"
    username=db.Column(db.String(50),primary_key=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    token=db.Column(db.String(50),nullable=False,unique=True)

    def __repr__(self):
        return f"<User {self.username}>"


    def save(self):
        db.session.add(self)
        db.session.commit()