from app import db
class Venue(db.Model):
    __tablename__ = 'venues'
    __table_args__ = {'schema': 'jcc_festival'} 
    name = db.Column(db.String(255), primary_key=True)
    address = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


    def __repr__(self):
        return f"<Venue(name={self.name}, address={self.address})>"
