from marshmallow import Schema, fields

class MovieSchema(Schema):
    name = fields.Str(required=True)  
    author = fields.Str(required=True)
    category = fields.Str()
    duration = fields.Int() 
    subtitles = fields.Str()
    nationality = fields.Str()
class MovieSchemaUpdate(Schema):
    author = fields.Str()
    category = fields.Str()
    duration = fields.Int() 
    subtitles = fields.Str()
    nationality = fields.Str()


class ProgramSchema(Schema):
    programme_name = fields.Str(required=True)  
    duration = fields.Int() 

class ProgramsMoviesSchema(Schema):
    programme_name = fields.Str(required=True)  
    movie_name = fields.Str(required=True)     

class VenueSchema(Schema):
    name = fields.Str(required=True)  
    address = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
class VenueSchemaUpdate(Schema):
    address = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

class AgendaSchema(Schema):
    id = fields.Int(required=True)  
    date = fields.Str(required=False)  
    venue_id = fields.Str(required=False)  
    hour = fields.Str(format="%H:%M",required=False)  
    movie_or_programme_name = fields.Str(required=False) 
class UpdateAgendaSchema(Schema):
    date = fields.Str(required=False)  
    venue_id = fields.Str(required=False)  
    hour = fields.Str(format="%H:%M",required=False)  
    movie_or_programme_name = fields.Str(required=False) 

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # This will be automatically generated
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)  # Don't expose the password hash
    role = fields.Str(validate=lambda x: x in ['user', 'admin'], default='user',dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
class loginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)  # Don't expose the password hash
    

class infoUserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(validate=lambda x: x in ['user', 'admin'], default='user',dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()

class LoginResponseSchema(Schema):
    message = fields.String()