from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Employee, Attendance, LeaveRequest, Payroll, Notification
from sqlalchemy import func, and_, or_

bp = Blueprint('employee', __name__, url_prefix='/employee')

def employee_required(f):
    """Decorator to ensure user is an employee"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.employee:
            flash('Access denied', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@employee_required
def dashboard():
    """Employee dashboard"""
    employee = current_user.employee
    
    # Get today's attendance
    today = date.today()
    today_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    # Get attendance summary (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    attendance_summary = db.session.query(
        Attendance.status,
        func.count(Attendance.id).label('count')
    ).filter(
        Attendance.employee_id == employee.id,
        Attendance.date >= thirty_days_ago
    ).group_by(Attendance.status).all()
    
    attendance_stats = {status: count for status, count in attendance_summary}
    
    # Get recent leave requests
    recent_leaves = LeaveRequest.query.filter_by(
        employee_id=employee.id
    ).order_by(LeaveRequest.created_at.desc()).limit(5).all()
    
    # Get latest payroll
    latest_payroll = Payroll.query.filter_by(
        employee_id=employee.id
    ).order_by(Payroll.year.desc(), Payroll.month.desc()).first()
    
    # Get unread notifications
    unread_notifications = Notification.query.filter_by(
        employee_id=employee.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('employee/dashboard.html',
                         employee=employee,
                         today_attendance=today_attendance,
                         attendance_stats=attendance_stats,
                         recent_leaves=recent_leaves,
                         latest_payroll=latest_payroll,
                         unread_notifications=unread_notifications)

@bp.route('/profile')
@employee_required
def profile():
    """View employee profile"""
    employee = current_user.employee
    return render_template('employee/profile.html', employee=employee)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@employee_required
def edit_profile():
    """Edit employee profile - limited fields"""
    employee = current_user.employee
    
    if request.method == 'POST':
        # Employees can only edit certain fields
        employee.phone = request.form.get('phone', '').strip()
        employee.address = request.form.get('address', '').strip()
        
        # Handle profile photo upload
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.employee_id}_{int(datetime.now().timestamp())}.{file.filename.rsplit('.', 1)[1].lower()}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    employee.profile_photo = filename
                else:
                    flash('Invalid file type. Only PNG, JPG, JPEG, GIF allowed.', 'error')
                    return render_template('employee/edit_profile.html', employee=employee)
        
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('employee.profile'))
    
    return render_template('employee/edit_profile.html', employee=employee)

@bp.route('/attendance')
@employee_required
def attendance():
    """View attendance records"""
    employee = current_user.employee
    page = request.args.get('page', 1, type=int)
    
    # Get attendance records
    attendance_records = Attendance.query.filter_by(
        employee_id=employee.id
    ).order_by(Attendance.date.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('employee/attendance.html',
                         employee=employee,
                         attendance_records=attendance_records)

@bp.route('/attendance/checkin', methods=['POST'])
@employee_required
def checkin():
    """Check in for today"""
    employee = current_user.employee
    today = date.today()
    
    # Check if already checked in
    existing_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    if existing_attendance:
        flash('You have already checked in today', 'warning')
        return redirect(url_for('employee.dashboard'))
    
    # Create attendance record
    attendance = Attendance(
        employee_id=employee.id,
        date=today,
        check_in=datetime.now().time(),
        status='Present'
    )
    db.session.add(attendance)
    db.session.commit()
    
    flash('Checked in successfully', 'success')
    return redirect(url_for('employee.dashboard'))

@bp.route('/attendance/checkout', methods=['POST'])
@employee_required
def checkout():
    """Check out for today"""
    employee = current_user.employee
    today = date.today()
    
    # Get today's attendance
    attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    if not attendance:
        flash('You have not checked in yet', 'error')
        return redirect(url_for('employee.dashboard'))
    
    if attendance.check_out:
        flash('You have already checked out today', 'warning')
        return redirect(url_for('employee.dashboard'))
    
    # Update checkout time
    attendance.check_out = datetime.now().time()
    attendance.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Checked out successfully', 'success')
    return redirect(url_for('employee.dashboard'))

@bp.route('/leave')
@employee_required
def leave():
    """View leave requests"""
    employee = current_user.employee
    page = request.args.get('page', 1, type=int)
    
    leave_requests = LeaveRequest.query.filter_by(
        employee_id=employee.id
    ).order_by(LeaveRequest.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('employee/leave.html',
                         employee=employee,
                         leave_requests=leave_requests,
                         leave_types=current_app.config['LEAVE_TYPES'])

@bp.route('/leave/apply', methods=['GET', 'POST'])
@employee_required
def apply_leave():
    """Apply for leave"""
    employee = current_user.employee
    
    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        reason = request.form.get('reason', '').strip()
        
        # Validation
        errors = []
        if not leave_type or leave_type not in current_app.config['LEAVE_TYPES']:
            errors.append('Please select a valid leave type')
        if not start_date_str or not end_date_str:
            errors.append('Please select start and end dates')
        if not reason:
            errors.append('Please provide a reason for leave')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('employee/apply_leave.html',
                                 employee=employee,
                                 leave_types=current_app.config['LEAVE_TYPES'])
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if start_date > end_date:
                flash('Start date must be before end date', 'error')
                return render_template('employee/apply_leave.html',
                                     employee=employee,
                                     leave_types=current_app.config['LEAVE_TYPES'])
            
            if start_date < date.today():
                flash('Start date cannot be in the past', 'error')
                return render_template('employee/apply_leave.html',
                                     employee=employee,
                                     leave_types=current_app.config['LEAVE_TYPES'])
            
            # Calculate days
            days = (end_date - start_date).days + 1
            
            # Create leave request
            leave_request = LeaveRequest(
                employee_id=employee.id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                days=days,
                reason=reason,
                status='Pending'
            )
            db.session.add(leave_request)
            db.session.commit()
            
            flash('Leave request submitted successfully', 'success')
            return redirect(url_for('employee.leave'))
        except ValueError:
            flash('Invalid date format', 'error')
            return render_template('employee/apply_leave.html',
                                 employee=employee,
                                 leave_types=current_app.config['LEAVE_TYPES'])
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to submit leave request: {str(e)}', 'error')
            return render_template('employee/apply_leave.html',
                                 employee=employee,
                                 leave_types=current_app.config['LEAVE_TYPES'])
    
    return render_template('employee/apply_leave.html',
                         employee=employee,
                         leave_types=current_app.config['LEAVE_TYPES'])

@bp.route('/payroll')
@employee_required
def payroll():
    """View payroll records"""
    employee = current_user.employee
    page = request.args.get('page', 1, type=int)
    
    payroll_records = Payroll.query.filter_by(
        employee_id=employee.id
    ).order_by(Payroll.year.desc(), Payroll.month.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('employee/payroll.html',
                         employee=employee,
                         payroll_records=payroll_records)

@bp.route('/payroll/<int:payroll_id>/slip')
@employee_required
def payroll_slip(payroll_id):
    """View salary slip"""
    employee = current_user.employee
    payroll = Payroll.query.filter_by(
        id=payroll_id,
        employee_id=employee.id
    ).first_or_404()
    
    return render_template('employee/payroll_slip.html',
                         employee=employee,
                         payroll=payroll)

@bp.route('/notifications')
@employee_required
def notifications():
    """View notifications"""
    employee = current_user.employee
    page = request.args.get('page', 1, type=int)
    
    notifications_query = Notification.query.filter_by(
        employee_id=employee.id
    ).order_by(Notification.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('employee/notifications.html',
                         employee=employee,
                         notifications=notifications_query)

@bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@employee_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    employee = current_user.employee
    notification = Notification.query.filter_by(
        id=notification_id,
        employee_id=employee.id
    ).first_or_404()
    
    notification.is_read = True
    db.session.commit()
    
    return redirect(url_for('employee.notifications'))

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
