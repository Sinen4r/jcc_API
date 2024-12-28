from flask_smorest import Blueprint
from flask import abort,request
import uuid
from flask.views import MethodView
from app import db
from schemas import ProgramSchema
from models.b import Program
from sqlalchemy.exc import SQLAlchemyError

blpProg=Blueprint("programs",__name__)

@blpProg.route('/program')
class program(MethodView):
    def get(self):
        """retrieve all Programs"""
        try:
            programs=Program.query.all()
            return{"programs":ProgramSchema(many=True).dump(programs)}
        except SQLAlchemyError as sq:
            abort(500,description=f"An error occurred: {str(sq)}")
    
    @blpProg.response(201, ProgramSchema)  # This will format the response with the schema
    @blpProg.arguments(ProgramSchema)
    def post(self,program_data):
        """add a new program"""
        program=Program(**program_data)
        try:
            db.session.add(program)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, description="An error occurred while inserting the agenda item.")
        # Return the newly created agenda as a response                         
        return program
@blpProg.route('/program/<program_id>')
class programbyID(MethodView):
    @blpProg.response(200,ProgramSchema)
    def get(self,program_id):
        """get a program by it s name"""
        try:
            program=Program.query.get(program_id)
            if program is None:
                abort(404,description=f"Agenda with ID {program_id} not found.")
        except SQLAlchemyError as e:
            abort(500, description=f"An error occurred: {str(e)}")
        return program
    
    @blpProg.arguments(ProgramSchema)
    @blpProg.response(200,ProgramSchema)
    def put(self,programupdatedData,program_id):
        """update a program"""
        program=Program.query.get(program_id)
        # programupdatedD=ProgramSchema().load(programupdatedData)
        for key, value in programupdatedData.items():
            setattr(program, key, value)
        db.session.commit()
        return  program     
    
    @blpProg.response(204)      
    def delete(self,program_id):
        """delete a program"""
        program=Program.query.get(program_id)
        if program is None:
            abort(404, description=f"Agenda with ID {program_id} not found.")
        try:
            db.session.delete(program)  
            db.session.commit() 
        except SQLAlchemyError:
            db.session.rollback() 
            abort(500, description="An error occurred while deleting the Program.")

        return "womp womp", 204  

