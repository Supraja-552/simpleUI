from flask_sqlalchemy  import SQLAlchemy
db=SQLAlchemy()
class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String(150),nullable=False)