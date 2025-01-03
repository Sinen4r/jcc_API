from flask_smorest import Blueprint
from flask import abort, render_template,request
import uuid
from flask.views import MethodView
from app import db
from schemas import MovieSchema,MovieSchemaUpdate
from models.a import Movie
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity,set_access_cookies
)
blpM=Blueprint("Movies",__name__)

@blpM.route('/movie')
class movie(MethodView):
    def get(self):
        try:
            movies=Movie.query.all()
            return{"movies":MovieSchema(many=True).dump(movies)}
        except SQLAlchemyError as sq:
            abort(500,description=f"An error occurred: {str(sq)}")
    
    @blpM.response(201, MovieSchema)  # This will format the response with the schema
    @jwt_required()   
    @blpM.arguments(MovieSchema)
    def post(self,movie_data):
        user = get_jwt() 
        if user["role"]=="admin":     
            movie=Movie(**movie_data)
            try:
                db.session.add(movie)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                abort(500, description="An error occurred while inserting the agenda item.")
            # Return the newly created agenda as a response                         
            return movie
        else:

            
            return render_template('agendas.html')
@blpM.route('/movie/<movie_id>')
class moviebyID(MethodView):
    @blpM.response(200,MovieSchema)
    def get(self,movie_id):
        try:
            movie=Movie.query.get(movie_id)
            if movie is None:
                abort(404,description=f"Agenda with ID {movie_id} not found.")
        except SQLAlchemyError as e:
            abort(500, description=f"An error occurred: {str(e)}")
        return movie
    
    @blpM.arguments(MovieSchemaUpdate)
    @blpM.response(200,MovieSchema)
    def put(self,movieupdatedData,movie_id):
        movie=Movie.query.get(movie_id)
        # movieupdatedD=MovieSchema().load(movieupdatedData)
        for key, value in movieupdatedData.items():
            setattr(movie, key, value)
        db.session.commit()
        return  movie     
    
    @blpM.response(204)      
    def delete(self,movie_id):
        movie=Movie.query.get(movie_id)
        if movie is None:
            abort(404, description=f"Agenda with ID {movie_id} not found.")
        try:
            db.session.delete(movie)  
            db.session.commit() 
        except SQLAlchemyError:
            db.session.rollback() 
            abort(500, description="An error occurred while deleting the movie.")

        return "womp womp", 204  