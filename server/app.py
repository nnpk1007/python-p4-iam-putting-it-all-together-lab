#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe


class Signup(Resource):
    
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        bio = data.get("bio")
        image_url = data.get("image_url")
        
        if not username or not password:
            return {"error":"Unprocessable Entity"}, 422
        # if the user is valid:
        # Save a new user to the database with their username, encrypted password, image URL, and bio.
        new_user = User(username=username, image_url=image_url, bio=bio)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        # Save the user's ID in the session object as user_id.
        session["user_id"] = new_user.id

        # Return a JSON response with the user's ID, username, image URL, and bio; and an HTTP status code of 201 (Created).
        respone = {
            "id": new_user.id,
            "username": new_user.username,
            "image_url": new_user.image_url,
            "bio": new_user.bio
        }

        return respone, 201


class CheckSession(Resource):
    
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.filter(User.id == user_id).first()
            response = {
                "id": user.id,
                "username": user.username
            }
            return response
        else:
            return {}, 401

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
