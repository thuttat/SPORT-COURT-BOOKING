from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect

from datetime import datetime

import cloudinary
from flask import  Blueprint, jsonify, request, current_app

from flask_login import current_user, login_required
from sqlalchemy import func

from bapp import dao, db, app
from bapp.decorators import admin_only
from bapp.models import Field, FieldType, UserRole, Booking, BookingStatus, Service, TimeSlots, Payment
from bapp.utils import validate_image


admin_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')


#########################################################
# Field Management
#########################################################


@admin_bp.route('/fields', methods=['GET'])
@login_required
@admin_only
def get_my_fields():
    page = request.args.get('page', 1, type=int)
    page_size = current_app.config.get('PAGE_SIZE', 6)

    pagination = dao.get_fields_by_user_paginated(current_user.id, page=page, page_size=page_size,include_inactive=True)

    results = []
    for f in pagination.items:  
        results.append({
            "id": f.id,
            "name": f.name,
            "field_type": f.field_type.name,
            "price_per_hour": float(f.price_per_hour),
            "description": f.description,
            "image": f.image,
            "is_active": f.is_active
        })

    return jsonify({
        "status": "success",
        "data": results,
        "pagination": {
            "total_items": pagination.total,  
            "total_pages": pagination.pages,
            "current_page": page,
            "has_next": pagination.has_next
        }
    }), 200


@admin_bp.route('/fields/<int:field_id>', methods=['GET'])
@login_required
@admin_only
def get_field_detail_for_admin(field_id):
    field = db.session.get(Field, field_id)
    if not field:
        return jsonify({"status": "error", "message": "Field not found"}), 404

    if field.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Access Denied"}), 403
    
    return jsonify({
        "status": "success",
        "data": {
            "id": field.id,
            "name": field.name,
            "field_type": field.field_type.name,
            "price_per_hour": float(field.price_per_hour),
            "description": field.description,
            "image": field.image,
            "is_active": field.is_active,
            "created_at": field.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    }), 200



@admin_bp.route('/fields', methods=['POST'])
@login_required
@admin_only
def add_new_field():
    name = request.form.get('name')
    price = request.form.get('price_per_hour')
    ftype_str = request.form.get('field_type')
    description = request.form.get('description')

    if not all([name, price, ftype_str]):
        return jsonify({
            "status": "error", 
            "message": "Missing required fields (name, price_per_hour, field_type)"
        }), 400

   
    if Field.query.filter_by(name=name).first():
        return jsonify({
            "status": "error", 
            "message": "Court name already exists"
        }), 400

    try:
        price_float = float(price)
        if price_float < 0:
            return jsonify({
                "status": "error", 
                "message": "Price must be a positive number"
            }), 400
    except ValueError:
        return jsonify({
            "status": "error", 
            "message": "Invalid price format"
        }), 400

    try:
        field_type_enum = FieldType[ftype_str.upper()]
    except KeyError:
        return jsonify({
            "status": "error", 
            "message": "Invalid field type"
        }), 400


    image_url = "https://res.cloudinary.com/dyupzyqwj/image/upload/v1774885674/siqqkjjrpotnvfjtoij7.jpg"
    file = request.files.get('image')
    if file:
        is_valid, error_msg = validate_image(file)
        if not is_valid:
            return jsonify({"status": "error", "message": error_msg}), 400
            
        res = cloudinary.uploader.upload(file)
        image_url = res['secure_url']
    try:
        field_type_enum = FieldType[ftype_str.upper()]
        new_f = dao.add_field(
            name=name,
            field_type=field_type_enum,
            price_per_hour=float(price),
            description=description,
            image=image_url,
            user_id=current_user.id
        )
        return jsonify({
            "status": "success",
            "message": "System successfully creates the new court.",
            "data": {
                "id": new_f.id,
                "name": new_f.name,
                "field_type": new_f.field_type.name,
                "price_per_hour": new_f.price_per_hour,
                "description": new_f.description,
                "image": new_f.image,
                "is_active": new_f.is_active,
                "created_at": new_f.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    


@admin_bp.route('/fields/<int:field_id>', methods=['PATCH'])
@login_required
@admin_only
def update_field(field_id):
    field = db.session.get(Field, field_id)
    if not field:
        return jsonify({"status": "error", "message": "Field not found"}), 404

    if field.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Access Denied"}), 403

    data_to_update = {}
    new_name = request.form.get('name')

    if new_name:
        if Field.query.filter(Field.name == new_name, Field.id != field_id).first():
            return jsonify({"status": "error", "message": "Court name already exists"}), 400
        data_to_update['name'] = new_name

    file = request.files.get('image')
    if file:
        is_valid, error_msg = validate_image(file)
        if not is_valid:
            return jsonify({"status": "error", "message": error_msg}), 400
            
        res = cloudinary.uploader.upload(file)
        data_to_update['image'] = res['secure_url']

    price = request.form.get('price_per_hour')
    if price:
        try:
            data_to_update['price_per_hour'] = float(price)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid price format"}), 400

    description = request.form.get('description')
    if description:
        data_to_update['description'] = description.strip()

    field_type = request.form.get('field_type')
    if field_type:
        try:
            data_to_update['field_type'] = FieldType[field_type.upper()]
        except KeyError:
            return jsonify({
                "status": "error",
                "message": "Invalid field type"
            }), 400

    is_active_str = request.form.get('is_active')
    if is_active_str is not None:
        data_to_update['is_active'] = is_active_str.lower() == 'true'

    if data_to_update:
        updated_field = dao.update_field(field_id, **data_to_update)

        if updated_field:
            return jsonify({
                "status": "success",
                "message": "Court updated successfully",
                "data": {
                    "id": updated_field.id,
                    "name": updated_field.name,
                    "field_type": updated_field.field_type.name,
                    "price_per_hour": float(updated_field.price_per_hour),
                    "description": updated_field.description,
                    "image": updated_field.image,
                    "is_active": updated_field.is_active
                }
            }), 200
    else:
        return jsonify({
            "status": "error", 
            "message": "No data provided to update"
        }), 400

    return jsonify({
        "status": "error", 
        "message": "Something went wrong during update"
    }), 500



@admin_bp.route('/fields/<int:field_id>', methods=['DELETE'])
@login_required
@admin_only
def delete_fields(field_id):
    field = db.session.get(Field, field_id)
    if not field:
        return jsonify({"status": "error", "message": "Field not found"}), 404

    if field.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Access Denied"}), 403

    now = datetime.now()
    upcoming_booking = Booking.query.filter(
        Booking.field_id == field_id,
        Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
    ).all()

    for b in upcoming_booking:
        start_datetime = datetime.combine(b.booking_date, b.time_slot.start_time)
        if start_datetime > now:
            return jsonify({
                "status": "error",
                "message": "Cannot delete this court because it has future bookings"
            }), 400
        
    dao.delete_field(field_id)

    return jsonify({
        "status": "success",
        "message": "Court deactivated successfully."
    }), 200




#########################################################
# Booking Management
#########################################################

@admin_bp.route('/bookings', methods=['GET'])
@login_required
@admin_only
def get_bookings():
    try:
        admin_id = current_user.id
        page = request.args.get('page', 1, type=int)
        page_size = current_app.config.get('PAGE_SIZE', 10)
        status_filter = request.args.get('status')

        query = Booking.query.join(Field).filter(Field.user_id == admin_id)
        if status_filter:
            try:
                status_enum = BookingStatus[status_filter.upper()]
                query = query.filter(Booking.status == status_enum)
            except KeyError:
                return jsonify({
                    "status": "error", 
                    "message": "Invalid status filter"
                }), 400

        pagination = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)

        results = []
        for b in pagination.items:
            results.append({
                "id": b.id,
                "customer_name": b.user.fullname if b.user else "Unknown",
                "customer_email": b.user.email if b.user else "", 
                "field_name": b.field.name,
                "field_type": b.field.field_type.name,
                "booking_date": b.booking_date.strftime("%Y-%m-%d"),
                "time_slot": b.time_slot.name,
                "duration": b.duration,
                "total_price": float(b.total_price),
                "status": b.status.name,
                "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify({
            "status": "success",
            "data": results,
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "page_size": page_size,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route('/bookings/<int:booking_id>/status', methods=['PATCH'])
@login_required
@admin_only
def update_booking_status(booking_id):
    try:
        booking = db.session.get(Booking, booking_id)
        if not booking:
            return jsonify({
                "status": "error", 
                "message": "Booking not found"
            }), 404

        if booking.field.user_id != current_user.id:
            return jsonify({
                "status": "error", 
                "message": "Access Denied. This booking does not belong to your courts."
            }), 403

        data = request.get_json() if request.is_json else request.form
        new_status_str = data.get('status')

        if not new_status_str:
            return jsonify({
                "status": "error", 
                "message": "Missing 'status' field"
            }), 400

        try:
            new_status_enum = BookingStatus[new_status_str.upper()]
        except KeyError:
            allowed_statuses = [e.name for e in BookingStatus]
            return jsonify({
                "status": "error", 
                "message": f"Invalid status. Allowed values: {allowed_statuses}"
            }), 400

        if booking.status == new_status_enum:
             return jsonify({
                 "status": "success", 
                 "message": "Booking status is already up to date."
             }), 200

        booking.status = new_status_enum
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Booking status updated successfully",
            "data": {
                "booking_id": booking.id,
                "new_status": booking.status.name
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500



@admin_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@login_required
@admin_only
def get_admin_booking_detail(booking_id): 
    try:
        booking = db.session.get(Booking, booking_id)
        if not booking:
            return jsonify({"status": "error", "message": "Booking not found"}), 404
            
        if booking.field.user_id != current_user.id:
            return jsonify({"status": "error", "message": "Access Denied"}), 403
            
        return jsonify({
            "status": "success",
            "data": {
                "id": booking.id,
                "customer_name": booking.user.fullname,
                "customer_phone": booking.user.username, 
                "field_name": booking.field.name,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
                "time_slot": booking.time_slot.name,
                "total_price": float(booking.total_price),
                "status": booking.status.name
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#########################################################
# Dashboard 
#########################################################

@admin_bp.route('/dashboard/summary', methods=['GET'])
@login_required
@admin_only
def get_dashboard_summary():
    try:
        admin_id = current_user.id
        today = datetime.now().date()
        total_fields = Field.query.filter_by(user_id=admin_id).count()
        active_fields = Field.query.filter_by(user_id=admin_id, is_active=True).count()
        total_bookings = Booking.query.join(Field).filter(Field.user_id == admin_id).count()
        bookings_today = Booking.query.join(Field).filter(
            Field.user_id == admin_id,
            Booking.booking_date == today
        ).count()

        return jsonify({
            "status": "success",
            "data": {
                "total_fields": total_fields,
                "active_fields": active_fields,
                "bookings_today": bookings_today,
                "total_bookings": total_bookings
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route('/dashboard/chart-sport', methods=['GET'])
@login_required
@admin_only
def get_chart_sport():
    try:
        admin_id = current_user.id
        
        sport_counts = db.session.query(
            Field.field_type, func.count(Field.id)
        ).filter(Field.user_id == admin_id).group_by(Field.field_type).all()

        results = []
        for f_type, count in sport_counts:
            results.append({
                "sport": f_type.name,
                "count": count
            })
 
        return jsonify({
            "status": "success",
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route('/dashboard/recent-bookings', methods=['GET'])
@login_required
@admin_only
def get_recent_bookings():
    try:
        admin_id = current_user.id
        recent_bookings = Booking.query.join(Field).filter(
            Field.user_id == admin_id
        ).order_by(Booking.created_at.desc()).limit(5).all()

        results = []
        for b in recent_bookings:
            results.append({
                "id": b.id,
                "customer_name": b.user.fullname if b.user else "Unknown", 
                "field_name": b.field.name,
                "booking_date": b.booking_date.strftime("%Y-%m-%d"),
                "time_slot": b.time_slot.name,
                "status": b.status.name,
                "total_price": float(b.total_price),
                "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify({
            "status": "success",
            "data": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============ADMIN SITE===============
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect('http://localhost:5173/login')

class ServiceView(AdminView):
    column_list = ['id', 'name', 'price', 'unit', 'is_active', 'updated_at']
    column_searchable_list = ['name']
    column_filters = ['name', 'price', 'unit']
    column_editable_list = ['name', 'price', 'unit', 'is_active']
    form_columns = ['name', 'price', 'unit', 'is_active']
    can_create = True
    can_delete = False

class TimeSlotsView(AdminView):
    column_list = ['id', 'name', 'start_time', 'end_time', 'price_multiplier', 'is_active', 'updated_at']
    column_searchable_list = ['name', 'start_time']
    column_filters = ['name', 'start_time', 'end_time']
    column_editable_list = ['name', 'start_time', 'end_time', 'price_multiplier', 'is_active']
    form_columns = ['name', 'start_time', 'end_time', 'price_multiplier', 'is_active']
    can_create = True
    can_delete = False

class PaymentView(AdminView):
    column_list = ['id', 'booking_id', 'amount', 'payment_method', 'payment_time', 'updated_at']
    column_searchable_list = ['id', 'booking_id']
    column_filters = ['booking_id', 'amount', 'payment_method']
    can_create = False
    can_edit = False
    can_delete = False

admin = Admin(app=app, name='Advanced system', url='/admin')

admin.add_view(TimeSlotsView(TimeSlots, db.session, name='Time Slots', endpoint='timeslots'))
admin.add_view(ServiceView(Service, db.session, name='Service', endpoint='service'))
admin.add_view(PaymentView(Payment, db.session, name='Payment', endpoint='payment'))