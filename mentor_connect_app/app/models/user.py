from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for mentor skills
mentor_skills = db.Table('mentor_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    @classmethod
    def insert_default_skills(cls):
        default_skills = [
            'Accounting', 'Business Strategy', 'Data Science', 'Digital Marketing',
            'Finance', 'Leadership', 'Machine Learning', 'Product Management',
            'Software Development', 'UI/UX Design', 'Web Development', 'Blockchain',
            'Artificial Intelligence', 'Cloud Computing', 'Cybersecurity',
            'Project Management', 'Sales', 'Technical Writing'
        ]
        for skill_name in default_skills:
            if not cls.query.filter_by(name=skill_name).first():
                skill = cls(name=skill_name)
                db.session.add(skill)
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    location = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(10), nullable=False, default='mentee')  # 'mentor' or 'mentee'
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(120), nullable=True, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Mentor specific fields
    hourly_rate = db.Column(db.Float, nullable=True)
    session_rate = db.Column(db.Float, nullable=True)  # Rate per 30 minutes
    title = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    
    # Relationships
    skills = db.relationship('Skill', secondary=mentor_skills, backref=db.backref('users', lazy='dynamic'))
    sessions_as_mentor = db.relationship('Session', backref='mentor', lazy=True, foreign_keys='Session.mentor_id')
    sessions_as_mentee = db.relationship('Session', backref='mentee', lazy=True, foreign_keys='Session.mentee_id')
    reviews_received = db.relationship('Review', backref='recipient', lazy=True, foreign_keys='Review.recipient_id')
    reviews_given = db.relationship('Review', backref='author', lazy=True, foreign_keys='Review.author_id')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"