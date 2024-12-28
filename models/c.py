from app import db
class ProgramsMovies(db.Model):
    __tablename__ = 'programs_movies'
    __table_args__ = {'schema': 'jcc_festival'} 
    programme_name = db.Column(db.String(255), db.ForeignKey('jcc_festival.programs.programme_name', ondelete="CASCADE"), primary_key=True)
    movie_name = db.Column(db.String(255), db.ForeignKey('jcc_festival.movies.name', ondelete="CASCADE"), primary_key=True)

    # Optional: Relationships to access related objects
    movie = db.relationship('Movie', backref='programs_moviess')
    program = db.relationship('Program', backref='programs_moviess')

    def __repr__(self):
        return f"<ProgramsMovies(programme_name={self.programme_name}, movie_name={self.movie_name})>"
