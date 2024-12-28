from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'jcc_festival'} 

    id = db.Column(db.Integer, primary_key=True)  # SERIAL PRIMARY KEY
    username = db.Column(db.String(50), nullable=False, unique=True)  # VARCHAR(50) NOT NULL UNIQUE
    email = db.Column(db.String(100), nullable=False, unique=True)  # VARCHAR(100) NOT NULL UNIQUE
    password_hash = db.Column(db.String(255), nullable=False)  # VARCHAR(255) NOT NULL
    role = db.Column(db.String(10), default='user', nullable=False)  # CHECK(role IN ('user', 'admin')) DEFAULT 'user'
    first_name = db.Column(db.String(50))  # VARCHAR(50)
    last_name = db.Column(db.String(50))  # VARCHAR(50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """Hash and store the password."""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the hashed password."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
