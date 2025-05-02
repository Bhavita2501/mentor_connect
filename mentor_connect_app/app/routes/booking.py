from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.session import Session
from app.models.payment import Payment
from app.forms.booking import BookingForm, SessionFeedbackForm
from datetime import datetime, timedelta

booking = Blueprint('booking', __name__)

@booking.route('/request-appointment', methods=['POST'])
@login_required
def request_appointment():
    if not current_user.is_authenticated or current_user.role != 'mentee':
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    mentor_id = data.get('mentor_id')
    message = data.get('message')
    
    if not mentor_id or not message:
        return jsonify({'error': 'Missing required fields'}), 400
        
    mentor = User.query.filter_by(id=mentor_id, role='mentor').first()
    if not mentor:
        return jsonify({'error': 'Mentor not found'}), 404
        
    session = Session(
        mentor_id=mentor_id,
        mentee_id=current_user.id,
        notes=message,
        status='requested'
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'message': 'Appointment request sent successfully'})

@booking.route('/approve-appointment/<int:session_id>', methods=['POST'])
@login_required
def approve_appointment(session_id):
    if current_user.role != 'mentor':
        flash('Only mentors can approve appointments.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    session = Session.query.get_or_404(session_id)
    
    if session.mentor_id != current_user.id:
        flash('You can only approve your own appointments.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    if session.status != 'requested':
        flash('This appointment cannot be approved.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    session.status = 'approved'
    db.session.commit()
    
    flash('Appointment approved successfully.', 'success')
    return redirect(url_for('booking.my_sessions'))

@booking.route('/reject-appointment/<int:session_id>', methods=['POST'])
@login_required
def reject_appointment(session_id):
    if current_user.role != 'mentor':
        flash('Only mentors can reject appointments.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    session = Session.query.get_or_404(session_id)
    
    if session.mentor_id != current_user.id:
        flash('You can only reject your own appointments.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    if session.status != 'requested':
        flash('This appointment cannot be rejected.', 'danger')
        return redirect(url_for('booking.my_sessions'))
        
    session.status = 'rejected'
    db.session.commit()
    
    flash('Appointment rejected.', 'info')
    return redirect(url_for('booking.my_sessions'))

@booking.route('/my-sessions', methods=['GET'])
@login_required
def my_sessions():
    if current_user.role == 'mentor':
        sessions = Session.query.filter_by(mentor_id=current_user.id).order_by(Session.created_at.desc()).all()
    else:
        sessions = Session.query.filter_by(mentee_id=current_user.id).order_by(Session.created_at.desc()).all()
    
    return render_template('booking/my_sessions.html', sessions=sessions)