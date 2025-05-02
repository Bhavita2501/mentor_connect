from flask import Blueprint, render_template, request, redirect, url_for
from app.models.user import User
from app import db
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_mentors = User.query.filter_by(role='mentor').limit(6).all()
    return render_template('index.html', featured_mentors=featured_mentors)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/mentors')
def mentors():
    if not current_user.is_authenticated or current_user.role != 'mentee':
        return redirect(url_for('main.index'))
        
    page = request.args.get('page', 1, type=int)
    min_rate = request.args.get('min_rate', type=float)
    max_rate = request.args.get('max_rate', type=float)
    
    query = User.query.filter_by(role='mentor')
    
    if min_rate:
        query = query.filter(User.hourly_rate >= min_rate)
    if max_rate:
        query = query.filter(User.hourly_rate <= max_rate)
    
    mentors = query.paginate(page=page, per_page=12)
    return render_template('mentors.html', mentors=mentors)

@main.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')