from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import User, Skill
from app.forms.profile import ProfileForm, MentorProfileForm
import os
from werkzeug.utils import secure_filename
import uuid

profile = Blueprint('profile', __name__)

def save_profile_image(form_picture):
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    
    upload_path = os.path.join(current_app.root_path, 'static/images/profile_pics')
    os.makedirs(upload_path, exist_ok=True)
    
    picture_path = os.path.join(upload_path, picture_filename)
    form_picture.save(picture_path)
    
    return picture_filename

@profile.route('/profile', methods=['GET'])
@login_required
def view_profile():
    user = User.query.get(current_user.id)
    return render_template('profile/view_profile.html', user=user)

@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_profile_image(form.profile_image.data)
            current_user.profile_image = picture_file
            
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.view_profile'))
    
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.location.data = current_user.location
        form.bio.data = current_user.bio
    
    return render_template('profile/edit_profile.html', form=form)

@profile.route('/profile/mentor', methods=['GET', 'POST'])
@login_required
def edit_mentor_profile():
    if current_user.role != 'mentor':
        flash('Only mentors can access this page.', 'danger')
        return redirect(url_for('profile.view_profile'))
    
    form = MentorProfileForm()
    
    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_profile_image(form.profile_image.data)
            current_user.profile_image = picture_file
            
        current_user.title = form.title.data
        current_user.company = form.company.data
        current_user.experience_years = form.experience_years.data
        current_user.hourly_rate = form.hourly_rate.data * 2  # Convert 30-min rate to hourly
        current_user.session_rate = form.hourly_rate.data  # 30-minute rate
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        
        # Handle skills as comma-separated text
        skill_names = [s.strip() for s in form.skills.data.split(',') if s.strip()]
        current_user.skills = []
        for skill_name in skill_names:
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                db.session.add(skill)
            current_user.skills.append(skill)
        
        db.session.commit()
        flash('Your mentor profile has been updated!', 'success')
        return redirect(url_for('profile.view_profile'))
    
    elif request.method == 'GET':
        form.title.data = current_user.title
        form.company.data = current_user.company
        form.experience_years.data = current_user.experience_years
        form.hourly_rate.data = current_user.session_rate  # Show 30-minute rate
        form.location.data = current_user.location
        form.bio.data = current_user.bio
        form.skills.data = ', '.join(skill.name for skill in current_user.skills)
    
    return render_template('profile/edit_mentor_profile.html', form=form)

@profile.route('/mentor/<int:mentor_id>', methods=['GET'])
def view_mentor(mentor_id):
    mentor = User.query.filter_by(id=mentor_id, role='mentor').first_or_404()
    return render_template('profile/view_mentor.html', mentor=mentor)