from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import random
import string
from app import db
from app.models import User, Employee, OTP, PreRegisteredEmployee
from app.email_utils import send_otp_email

bp = Blueprint('auth', __name__, url_prefix='/auth')


def generate_otp():
    """Generate a random OTP code"""
    otp_length = current_app.config.get('OTP_LENGTH', 6)
    return ''.join(random.choices(string.digits, k=otp_length))


def create_otp(email, purpose='login'):
    """Create and save OTP for email"""
    # Invalidate any existing OTPs for this email and purpose
    existing_otps = OTP.query.filter_by(email=email, purpose=purpose, is_used=False).all()
    for otp in existing_otps:
        otp.is_used = True
    
    # Generate new OTP
    otp_code = generate_otp()
    expiry_minutes = current_app.config.get('OTP_EXPIRY_MINUTES', 10)
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    
    # Save OTP to database
    otp = OTP(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    db.session.add(otp)
    db.session.commit()
    
    return otp_code


def verify_otp_code(email, otp_code, purpose='login'):
    """Verify OTP code"""
    otp = OTP.query.filter_by(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        is_used=False
    ).first()
    
    if otp and otp.is_valid():
        otp.is_used = True
        db.session.commit()
        return True
    return False

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'Employee')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Validation
        errors = []
        if not employee_id:
            errors.append('Employee ID is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if not first_name or not last_name:
            errors.append('First name and last name are required')
        
        # Check if employee is pre-registered by HR
        pre_registered = PreRegisteredEmployee.query.filter_by(employee_id=employee_id).first()
        if not pre_registered:
            errors.append('Employee ID not found. Please contact HR to add your employee ID first.')
        elif pre_registered.is_registered:
            errors.append('This employee ID has already been registered.')
        elif pre_registered.email.lower() != email:
            errors.append(f'Email does not match the one registered by HR for this employee ID. Please use the correct email.')
        
        # Check if user already exists
        if User.query.filter_by(employee_id=employee_id).first():
            errors.append('Employee ID already registered')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        # Create user
        try:
            user = User(
                employee_id=employee_id,
                email=email,
                role='Employee'  # Always Employee for self-registration
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            
            # Create employee profile with pre-registered data
            employee = Employee(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                department=pre_registered.department,
                designation=pre_registered.designation,
                date_of_joining=datetime.utcnow().date()
            )
            db.session.add(employee)
            
            # Mark as registered
            pre_registered.is_registered = True
            pre_registered.registered_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login - Step 1: Email and Password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact HR.', 'error')
                return render_template('auth/login.html')
            
            # Generate and send OTP
            otp_code = create_otp(email, 'login')
            send_otp_email(email, otp_code, 'login')
            flash('OTP has been sent to your email. Please check your inbox.', 'success')
            
            # Store email in session for OTP verification
            session['otp_email'] = email
            session['otp_purpose'] = 'login'
            
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')


@bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """User login - Step 2: OTP Verification"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = session.get('otp_email')
    purpose = session.get('otp_purpose', 'login')
    
    if not email:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()
        
        if not otp_code:
            flash('Please enter the OTP code', 'error')
            return render_template('auth/verify_otp.html', email=email)
        
        if verify_otp_code(email, otp_code, purpose):
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                login_user(user, remember=True)
                session.permanent = True
                
                # Clear OTP session data
                session.pop('otp_email', None)
                session.pop('otp_purpose', None)
                
                flash(f'Welcome back, {user.employee.full_name}!', 'success')
                
                # Redirect based on role
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                elif user.is_admin():
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('employee.dashboard'))
            else:
                flash('User not found', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'error')
    
    return render_template('auth/verify_otp.html', email=email)


@bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP to user's email"""
    email = session.get('otp_email')
    purpose = session.get('otp_purpose', 'login')
    
    if not email:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('auth.login'))
    
    # Generate and send new OTP
    otp_code = create_otp(email, purpose)
    send_otp_email(email, otp_code, purpose)
    flash('A new OTP has been sent to your email.', 'success')
    
    return redirect(url_for('auth.verify_otp'))

@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))
