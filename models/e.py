from app import db

class Agenda(db.Model):
    __tablename__ = 'agenda'
    __table_args__ = {'schema': 'jcc_festival'} 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    venue_id = db.Column(db.String(255), db.ForeignKey('jcc_festival.venues.name'), nullable=False)  # Foreign key to venues(name)
    hour = db.Column(db.Time, nullable=False)
    movie_or_programme_name = db.Column(db.String(255), nullable=True)

    # Optional: Relationship to link to venues table
    venue = db.relationship('Venue', backref='agenda_list', lazy=True)