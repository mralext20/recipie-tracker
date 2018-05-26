from flask_login import UserMixin
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('chefs.id'), nullable=False)
    author = db.relationship("Chef", backref=db.backref('recipies', lazy=True))

    def __repr__(self):
        return f"<Recipe id={self.id} title={self.title}>"

    @property
    def list_ingredients(self):
        return self.ingredients.split('\r\n')

    @property
    def list_instructions(self):
        return self.instructions.split('\r\n')


class Chef(UserMixin, db.Model):
    __tablename__ = "chefs"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    displayname = db.Column(db.Text, nullable=False)
    passkey = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.passkey = generate_password_hash(password)

    def check_password(self, password):
        if self.id == 1:
            if self.admin == False:
                self.admin = True
                db.session.add(self)
                db.session.commit()
        return check_password_hash(self.passkey, password)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


@login.user_loader
def load_chef(uid):
    return Chef.query.get(int(uid))

