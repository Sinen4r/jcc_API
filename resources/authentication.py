from flask_smorest import Blueprint
from flask import abort, render_template,request,make_response,jsonify, url_for,session
import uuid
from flask.views import MethodView
from app import db
from schemas import UserSchema,loginSchema,infoUserSchema,LoginResponseSchema
from models.f import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies
)
import random
from resources.googleOath import google

blpAuth=Blueprint("authentication",__name__)

# oauth = OAuth()
# google = oauth.register(
#     'google',
#     client_id='84497968223-sq4jgsb2gu8tlgpqavlb8n0gc395ir5v.apps.googleusercontent.com',
#     client_secret='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',
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     api_base_url='https://www.googleapis.com/oauth2/v2/',
#     client_kwargs={'scope': 'openid profile email'},
#     authorize_state="5e884898da28047151d0e56f8dc6292773603d0d6aabbddc73e06ef7ff70e2c4"
# )

# # Flask app will initialize OAuth during app setup
# def init_oauth(app):
#     oauth.init_app(app)

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
        
        access_token = create_access_token(identity=username,additional_claims={"role": user.role})
        response = make_response(jsonify({"msg": "Login successful"}))
        print(access_token)
        # Set the JWT as an HTTP-only cookie
        set_access_cookies(response, access_token)
        return {"message" : user.role}
    def get(self):
        return render_template('login.html')

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
    def get(self):
        return render_template('signup.html')
@blpAuth.route("/info/<username>")
class create(MethodView):
    @blpAuth.response(200,infoUserSchema)
    def get(self,username):
        user=User.query.get(username)
        if user is None:
            abort(404,description=f"user with username {username} not found.")        
        return user

@blpAuth.route("/admin")
class authentication(MethodView):
    def get(self):
            return render_template('admin.html')

@blpAuth.route('/auth/google')
def google_login():
    
    redirect_uri = url_for('authentication.google_callback', _external=True)
    # redirect_uri="http://localhost:5000/callback"
    state = session.get('state')
    print("-----------------------------",state)

    return google.authorize_redirect(redirect_uri)

@blpAuth.route('/callback')
def google_callback():
    print(f"Session State: {session.get('state')}")  # Debugging: print session state
    # Retrieve the token after successful authentication
    token = google.authorize_access_token()
    if not token:
        abort(400, 'State missing or invalid')
    
    # Fetch user info from Google
    user_info = google.get('userinfo').json()

    # Extract user information
    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')
    username = first_name  + last_name+str(random.randint(1,999))  

    # Example: Creating a dictionary with the required fields
    user_data = {
        "username": username,
        "email": email,
        "password_hash": "00001232145s@",  
        "last_name": last_name
    }

    new_user = User(**user_data)  
    new_user.set_password(user_data['password_hash'])

    db.session.add(new_user)
    db.session.commit()

    return render_template('agendas.html') 