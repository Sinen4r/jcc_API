from app import db

class Program(db.Model):
    __tablename__ = 'programs'
    __table_args__ = {'schema': 'jcc_festival'} 
    programme_name = db.Column(db.String(255), primary_key=True)
    duration = db.Column(db.Integer, nullable=True)  # Duration in minutes


    def __repr__(self):
        return f"<Program(programme_name={self.programme_name}, duration={self.duration})>"
