from flask_smorest import Blueprint
from flask import abort,request
import uuid
from flask.views import MethodView
from app import db
from schemas import VenueSchema,VenueSchemaUpdate
from models.d import Venue
from sqlalchemy.exc import SQLAlchemyError

blpVen=Blueprint("Venues",__name__)

@blpVen.route('/Venue')
class Venues(MethodView):
    def get(self):
        """retrieve all Venues"""
        try:
            Venues=Venue.query.all()
            return{"Venues":VenueSchema(many=True).dump(Venues)}
        except SQLAlchemyError as sq:
            abort(500,description=f"An error occurred: {str(sq)}")
    
    @blpVen.response(201, VenueSchema)  # This will format the response with the schema
    @blpVen.arguments(VenueSchema)
    def post(self,Venue_data):
        """add a new Venue"""
        Venues=Venue(**Venue_data)
        try:
            db.session.add(Venues)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, description="An error occurred while inserting the agenda item.")
        # Return the newly created agenda as a response                         
        return Venues
@blpVen.route('/Venue/<Venue_id>')
class VenuebyID(MethodView):
    @blpVen.response(200,VenueSchema)
    def get(self,Venue_id):
        """get a Venue by it s name"""
        try:
            Venues=Venue.query.get(Venue_id)
            if Venues is None:
                abort(404,description=f"Agenda with ID {Venue_id} not found.")
        except SQLAlchemyError as e:
            abort(500, description=f"An error occurred: {str(e)}")
        return Venues
    
    @blpVen.arguments(VenueSchemaUpdate)
    @blpVen.response(200,VenueSchema)
    def put(self,VenueupdatedData,Venue_id):
        """update a Venue"""
        Venues=Venue.query.get(Venue_id)
        # VenueupdatedD=VenueSchema().load(VenueupdatedData)
        for key, value in VenueupdatedData.items():
            setattr(Venues, key, value)
        db.session.commit()
        return  Venues     
    
    @blpVen.response(204)      
    def delete(self,Venue_id):
        """delete a Venue"""
        Venues=Venue.query.get(Venue_id)
        if Venues is None:
            abort(404, description=f"Venue with ID {Venue_id} not found.")
        try:
            db.session.delete(Venues)  
            db.session.commit() 
        except SQLAlchemyError:
            db.session.rollback() 
            abort(500, description="An error occurred while deleting the Venue.")

        return "womp womp", 204  