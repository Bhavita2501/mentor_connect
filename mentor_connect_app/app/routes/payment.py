from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.models.session import Session
import stripe
import os

payment = Blueprint('payment', __name__)

@payment.route('/payment/<int:payment_id>', methods=['GET'])
@login_required
def process_payment(payment_id):
    payment_record = Payment.query.get_or_404(payment_id)
    session = Session.query.get(payment_record.session_id)
    
    # Check if user is the mentee in this session
    if current_user.id != session.mentee_id:
        flash('You do not have permission to access this payment.', 'danger')
        return redirect(url_for('booking.my_sessions'))
    
    # Check if payment is still pending
    if payment_record.status != 'pending':
        flash('This payment has already been processed.', 'info')
        return redirect(url_for('booking.session_detail', session_id=session.id))
    
    # Setup Stripe
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')
    
    return render_template('payment/checkout.html', 
                          payment=payment_record,
                          session=session,
                          stripe_public_key=stripe_public_key)

@payment.route('/payment/create-intent/<int:payment_id>', methods=['POST'])
@login_required
def create_payment_intent(payment_id):
    payment_record = Payment.query.get_or_404(payment_id)
    session = Session.query.get(payment_record.session_id)
    
    # Check if user is the mentee in this session
    if current_user.id != session.mentee_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Setup Stripe
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    
    try:
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(payment_record.amount * 100),  # Stripe uses cents
            currency=payment_record.currency,
            metadata={
                'payment_id': payment_record.id,
                'session_id': session.id
            }
        )
        
        return jsonify({
            'clientSecret': intent.client_secret
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment.route('/payment/confirm', methods=['POST'])
@login_required
def confirm_payment():
    data = request.json
    payment_intent_id = data.get('payment_intent_id')
    payment_id = data.get('payment_id')
    
    payment_record = Payment.query.get_or_404(payment_id)
    session = Session.query.get(payment_record.session_id)
    
    # Check if user is the mentee in this session
    if current_user.id != session.mentee_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Update payment record
    payment_record.status = 'completed'
    payment_record.stripe_payment_id = payment_intent_id
    
    # Update session status
    session.status = 'confirmed'
    
    db.session.commit()
    
    return jsonify({'success': True})

@payment.route('/payment/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_id = payment_intent['metadata'].get('payment_id')
        
        if payment_id:
            payment_record = Payment.query.get(int(payment_id))
            if payment_record:
                payment_record.status = 'completed'
                session = Session.query.get(payment_record.session_id)
                session.status = 'confirmed'
                db.session.commit()
    
    return jsonify({'success': True})