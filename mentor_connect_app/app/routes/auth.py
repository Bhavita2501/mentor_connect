from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from app import db, google
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.password = form.password.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/login/google')
def google_login():
    return google.authorize(callback=url_for('auth.google_authorized', _external=True))

@auth.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ), 'danger')
        return redirect(url_for('auth.login'))

    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    
    # Check if user exists
    user = User.query.filter_by(email=me.data['email']).first()
    
    if not user:
        # Create new user
        user = User(
            username=me.data['email'].split('@')[0],
            email=me.data['email'],
            first_name=me.data.get('given_name'),
            last_name=me.data.get('family_name'),
            role='mentee'  # Default role for Google sign-ups
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    flash('Successfully signed in with Google!', 'success')
    return redirect(url_for('main.index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')