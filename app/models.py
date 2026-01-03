from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Employee')  # Admin, HR, Employee
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    employee = db.relationship('Employee', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role in ['Admin', 'HR']
    
    def __repr__(self):
        return f'<User {self.employee_id}>'

class Employee(db.Model):
    """Employee profile model"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_photo = db.Column(db.String(255), default='default.jpg')
    
    # Job Information
    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    date_of_joining = db.Column(db.Date)
    employment_type = db.Column(db.String(20))  # Full-time, Part-time, Contract
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    
    # Status
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Terminated
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')
    attendance_records = db.relationship('Attendance', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    payroll_records = db.relationship('Payroll', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='employee', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'

class Attendance(db.Model):
    """Attendance tracking model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    status = db.Column(db.String(20), nullable=False)  # Present, Absent, Half-day, Leave
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='_employee_date_uc'),)
    
    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.date}>'

class LeaveRequest(db.Model):
    """Leave request model"""
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    admin_comment = db.Column(db.Text)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} - {self.status}>'

class Payroll(db.Model):
    """Payroll model"""
    __tablename__ = 'payroll'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Salary Structure
    basic_salary = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, default=0)  # House Rent Allowance
    da = db.Column(db.Float, default=0)  # Dearness Allowance
    ta = db.Column(db.Float, default=0)  # Travel Allowance
    medical_allowance = db.Column(db.Float, default=0)
    other_allowances = db.Column(db.Float, default=0)
    
    # Deductions
    pf = db.Column(db.Float, default=0)  # Provident Fund
    tax = db.Column(db.Float, default=0)
    insurance = db.Column(db.Float, default=0)
    other_deductions = db.Column(db.Float, default=0)
    
    # Period
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    # Totals
    gross_salary = db.Column(db.Float)
    net_salary = db.Column(db.Float)
    
    # Status
    status = db.Column(db.String(20), default='Pending')  # Pending, Processed, Paid
    payment_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'month', 'year', name='_employee_month_year_uc'),)
    
    def calculate_totals(self):
        """Calculate gross and net salary"""
        self.gross_salary = (
            self.basic_salary + self.hra + self.da + self.ta + 
            self.medical_allowance + self.other_allowances
        )
        total_deductions = self.pf + self.tax + self.insurance + self.other_deductions
        self.net_salary = self.gross_salary - total_deductions
    
    def __repr__(self):
        return f'<Payroll {self.employee_id} - {self.month}/{self.year}>'

class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.title}>'

class OTP(db.Model):
    """OTP model for email verification"""
    __tablename__ = 'otp'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    otp_code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(20), nullable=False)  # login, registration, reset_password
    is_used = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        """Check if OTP is valid and not expired"""
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def __repr__(self):
        return f'<OTP {self.email} - {self.purpose}>'

class PreRegisteredEmployee(db.Model):
    """Pre-registered employees by HR - required before employee can sign up"""
    __tablename__ = 'pre_registered_employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    is_registered = db.Column(db.Boolean, default=False)  # True when employee completes signup
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registered_at = db.Column(db.DateTime)
    
    admin_user = db.relationship('User', foreign_keys=[added_by])
    
    def __repr__(self):
        return f'<PreRegisteredEmployee {self.employee_id} - {self.email}>'

