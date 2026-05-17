import hashlib
import hmac
import json
import urllib.parse
from datetime import datetime
import requests

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required

from bapp import db
from bapp.models import Booking, Payment, PaymentMethod, BookingStatus
from bapp.utils import  generate_vnpay_url

payment_bp = Blueprint('payment_api', __name__, url_prefix='/api/payments')

@payment_bp.route('/create', methods=['POST'])
@login_required
def create_payment():
    try:
        data = request.get_json()
        booking_id = data.get('booking_id')
        method_str = data.get('payment_method') 

      
        booking = db.session.get(Booking, booking_id)
        if not booking:
            return jsonify({
                "status": "error", 
                "message": "Booking not found"
            }), 404
        
        if booking.user_id != current_user.id:
            return jsonify({
                "status": "error", 
                "message": "Access Denied"
            }), 403
            
        if booking.status != BookingStatus.PENDING:
            return jsonify({
                "status": "error", 
                "message": "Booking is already processed"
            }), 400
        
        existing_payment = Payment.query.filter_by(booking_id=booking.id).first()
        if existing_payment:
            return jsonify({
                "status": "error",
                "message": "Payment already exists for this booking"
            }), 409 

        try:
            payment_method = PaymentMethod[method_str.upper()]
        except KeyError:
            return jsonify({"status": "error", "message": "Invalid payment method"}), 400

    
        if payment_method == PaymentMethod.CASH:
            new_payment = Payment(
                amount=booking.total_price,
                payment_method=PaymentMethod.CASH,
                booking_id=booking.id
            )
            db.session.add(new_payment)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": "Cash payment recorded. Please pay at the court.",
                "data": {"redirect_url": None} 
            }), 200

     
        elif payment_method == PaymentMethod.VNPAY:
            vnpay_url = generate_vnpay_url(booking, request.remote_addr)
            return jsonify({
                "status": "success", 
                "message": "Redirecting to VNPay...",
                "data": {"payUrl": vnpay_url} 
            }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    


@payment_bp.route('/vnpay/return', methods=['GET'])
def vnpay_return():
    params = request.args.to_dict()
   
    received_hash = params.pop('vnp_SecureHash', '')
    params.pop('vnp_SecureHashType', None) 
    
    sorted_params = sorted(params.items())
    query_string = ''
    
    for key, val in sorted_params:
        value = str(val)
        query_string = query_string + urllib.parse.quote_plus(key) + '=' + urllib.parse.quote_plus(value) + '&'
        
    query_string = query_string[:-1] 
    
    expected_hash = hmac.new(
        b"DWNZDYT99VTGXXDDMD59VNBGR6ROY5HP",
        query_string.encode('utf-8'),
        hashlib.sha512
    ).hexdigest()
    
    if not hmac.compare_digest(expected_hash, received_hash):
        return jsonify({
            "status": "error", 
            "message": "Invalid signature"
        }), 400

    response_code = params.get('vnp_ResponseCode')
    booking_id = int(params.get('vnp_TxnRef'))
    
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({
            "status": "error", 
            "message": "Booking not found"
        }), 404

    if response_code == '00':  
        if not Payment.query.filter_by(booking_id=booking_id).first():
            payment = Payment(
                amount=booking.total_price,
                payment_method=PaymentMethod.VNPAY,
                booking_id=booking_id
            )
            db.session.add(payment)
            booking.status = BookingStatus.CONFIRMED
            db.session.commit()
        return jsonify({
            "status": "success", 
            "message": "Payment successful"
        }), 200
    else:
        return jsonify({
            "status": "error", 
            "message": f"Payment failed. Code: {response_code}"
        }), 400