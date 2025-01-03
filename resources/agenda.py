from flask_smorest import Blueprint
from flask import abort,render_template
import uuid
from flask.views import MethodView
from app import db
from schemas import AgendaSchema,UpdateAgendaSchema,AgendaDateSchema
from models.e import Agenda
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity,set_access_cookies
)

blp=Blueprint("agenda",__name__)

@blp.route("/agenda")
class agenda(MethodView):
    def get(self):
        try:
            
            agendas = Agenda.query.limit(5).all()
            print(str(agendas))
            # Use Marshmallow schema to serialize the result
            return {"agendas": AgendaSchema(many=True).dump(agendas)}
        except Exception as e:
            abort(500, description=f"An error occurred: {str(e)}")

    @blp.arguments(AgendaSchema)  # This will validate and deserialize the incoming JSON data
    @jwt_required()   
    @blp.response(201, AgendaSchema)  # This will format the response with the schema
    def post(self, agenda_data):
        user = get_jwt() 
        print("sssssssssssss")
        print(user)
        if user["role"]=="admin":        
            # Create a new Agenda object using the validated data
            agenda = Agenda(**agenda_data)

            try:
                # Add the new agenda to the database and commit the transaction
                db.session.add(agenda)
                db.session.commit()
            except SQLAlchemyError:
                # If there is an error (e.g., a database constraint violation), we handle it here
                db.session.rollback()
                abort(500, description="An error occurred while inserting the agenda item.")
            # Return the newly created agenda as a response
            return agenda
        else:
            return render_template('agendas.html')

@blp.route("/agenda/<agenda_id>")
class agendabyID(MethodView):
    @blp.response(200, AgendaSchema)
    def get(self,agenda_id):
        movie=Agenda.query.get(agenda_id)
        if movie is None:
            abort(404, description=f"Agenda with ID {agenda_id} not found.")
        # Return the agenda object; Flask-Smorest will handle serialization
        return movie
    
    
    @jwt_required()    
    @blp.arguments(UpdateAgendaSchema)  # No partial=True here
    @blp.response(200, AgendaSchema)
    def patch(self, agenda_data, agenda_id):
        user = get_jwt() 

        if user["role"]=="admin":   
            # Fetch the agenda by its ID
            agenda = Agenda.query.get(agenda_id)
            if not agenda:
                abort(404, description=f"Agenda with ID {agenda_id} not found.")
            
            # Apply partial update
            agenda_data = UpdateAgendaSchema().load(agenda_data, partial=True)  # Handle partial updates here
            
            # Update the agenda fields
            for key, value in agenda_data.items():
                setattr(agenda, key, value)
            
            db.session.commit()  # Save changes to the database
            
            return agenda 
        else:
            return render_template('agendas.html')


    @blp.response(204)  # No content, since we're just deleting the resource
    @jwt_required()
    def delete(self, agenda_id):
        user = get_jwt() 
        if user["role"]=="admin":
            # Query the database for the agenda with the given agenda_id
            agenda = Agenda.query.get(agenda_id)

            # If no agenda is found, return a 404 error
            if agenda is None:
                abort(404, description=f"Agenda with ID {agenda_id} not found.")

            # Delete the agenda from the database
            try:
                db.session.delete(agenda)  # Delete the agenda object from the session
                db.session.commit()  # Commit the transaction
            except SQLAlchemyError:
                db.session.rollback()  # Rollback the transaction in case of error
                abort(500, description="An error occurred while deleting the agenda.")
    
        # No content to return, just a successful 204 response
            return "womp womp", 204  # 204 No Content is a standard response for successful deletions
        else:
            return render_template('agendas.html')



@blp.route("/agenda/<venue_ids>/<int:count>")
class agendabyVenue(MethodView):
    def get(self,venue_ids,count):
        print(f"Received request with AGORA={venue_ids} and count={count}")

        movie = Agenda.query.filter_by(venue_id=venue_ids).limit(count).all()
        print(str(movie))
        if movie is None:
            abort(404, description=f"Agenda with ID {id} not found.")
        # Return the agenda object; Flask-Smorest will handle serialization
        return {"agendas": AgendaSchema(many=True).dump(movie)}
    


@blp.route("/agenda/movie/<movie_id>/<int:count>")
class agendabyMovie(MethodView):
    def get(self, movie_id, count):
        print(f"Received request with movie_id={movie_id} and cont={count}")
        
        # Check if the movie_id exists in the query
        movie = Agenda.query.filter_by(movie_or_programme_name=movie_id).limit(count).all()
        print("ss")
        print(f"Query result: {str(Agenda.query.filter_by(movie_or_programme_name=movie_id).limit(count))}")  # Debugging the query result
        
        # Check if any movie was found
        if not movie:  # Checking if the list is empty
            print("No agendas found for this movie ID.")
            abort(404, description=f"Agenda with movie ID {movie_id} not found.")
        
        # Return the agenda object; Flask-Smorest will handle serialization
        return {"agendas": AgendaSchema(many=True).dump(movie)}

@blp.route("/agenda/date")
class agendabydate(MethodView):
    @blp.arguments(AgendaDateSchema)
    def post(self,agenda_data):

            date = agenda_data['date']
            hour = agenda_data['hour']
            venue_id = agenda_data.get('venue_id')
            movie_or_programme_name = agenda_data.get('movie_or_programme_name')

            query = Agenda.query.filter(Agenda.date == date, Agenda.hour == hour)

            if venue_id is not None:
                query = query.filter(Agenda.venue_id == venue_id)
            if movie_or_programme_name:
                query = query.filter(Agenda.movie_or_programme_name.ilike(f"%{movie_or_programme_name}%"))
            results = query.all()
            return {"agendas": AgendaSchema(many=True).dump(results)}  # Replace with actual response format


@blp.route("/agendas")
class agenda(MethodView):
    def get(self):
        return render_template('agendas.html')
