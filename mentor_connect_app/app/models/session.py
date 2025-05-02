from app import db
from datetime import datetime

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='requested')  # requested, approved, rejected, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    payment = db.relationship('Payment', backref='session', lazy=True, uselist=False)
    
    def __repr__(self):
        return f"Session(Mentor: {self.mentor_id}, Mentee: {self.mentee_id}, Status: {self.status})"