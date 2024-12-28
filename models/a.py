from app import db

class Movie(db.Model):
    __tablename__ = 'movies'
    __table_args__ = {'schema': 'jcc_festival'} 
    name = db.Column(db.String(255), primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    subtitles = db.Column(db.String(100), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Movie(name={self.name}, author={self.author}, category={self.category})>"
