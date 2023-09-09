from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship, validates

from config import db, bcrypt


class User(db.Model, SerializerMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    # have many recipes.
    recipes = relationship("Recipe", backref="user")

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be present")
        
        return username
        
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

    
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # title must be present.
    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must be present")
        
        return title
    # instructions must be present and at least 50 characters long.
    @validates("instructions")
    def validate_instruction(self, key, instruction):
        if not instruction:
            raise ValueError("Instruction must be present")
        if len(instruction) <= 50:
            raise ValueError("Instruction must be at least 50 characters long")

        return instruction

    def __repr__(self):
        return f"Recipe {self.id} {self.title}"
