from flask_smorest import Blueprint
from flask import abort,request
import uuid
from flask.views import MethodView
from app import db
from schemas import UserSchema,loginSchema,infoUserSchema,LoginResponseSchema
from models.f import User
from sqlalchemy.exc import SQLAlchemyError


blpAuth=Blueprint("authentication",__name__)

@blpAuth.route("/login")
class authentication(MethodView):
    @blpAuth.response(200,LoginResponseSchema)
    @blpAuth.arguments(loginSchema)  # This will validate and deserialize the incoming JSON data    
    def post(self,loginData):
        """login  to the api"""
        username = loginData["username"]
        password = loginData["password"]

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            abort(404,description=" User doesn't exist") 

        if not user.check_password(password):
            abort(401,description="Incorrect password")  
        return {"message": "Login successful"}
@blpAuth.route("/createUser")
class create(MethodView):
    @blpAuth.response(200,LoginResponseSchema)
    @blpAuth.arguments(UserSchema)  # This will validate and deserialize the incoming JSON data    
    def post(self,loginData):
        """create a user """
        password = loginData.get('password')
        loginData.pop('password', None)
        newUser = User(**loginData)
        newUser.set_password(password)
        
        # Add the new user to the session and commit to the database
        db.session.add(newUser)
        db.session.commit()
        return {"message": "sign up successful"}
@blpAuth.route("/info/<username>")
class create(MethodView):
    @blpAuth.response(200,infoUserSchema)
    def get(self,username):
        user=User.query.get(username)
        if user is None:
            abort(404,description=f"user with username {username} not found.")        
        return user
