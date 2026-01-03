# Dayflow - Human Resource Management System

![Dayflow HRMS](https://img.shields.io/badge/Dayflow-HRMS-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)

> **Every workday, perfectly aligned.**

A complete, production-ready Human Resource Management System built with Python Flask, featuring employee management, attendance tracking, leave management, payroll processing, and comprehensive reporting.

## 🌟 Features

### 🔐 Authentication & Authorization
- Secure user registration and login
- Password hashing with Werkzeug
- Role-based access control (Admin / HR / Employee)
- Session-based authentication

### 👥 Employee Management
- Complete employee profile management
- Personal, job, and salary information
- Profile photo upload
- Employee status tracking
- Department and designation management

### ⏰ Attendance Management
- Check-in/Check-out functionality
- Multiple attendance statuses (Present, Absent, Half-day, Leave)
- Daily and historical attendance views
- Admin can mark/modify attendance
- Attendance reports

### 📅 Leave Management
- Employee leave applications
- Multiple leave types (Sick, Casual, Annual, etc.)
- Leave approval workflow
- Status tracking (Pending, Approved, Rejected)
- Admin comments and feedback
- Automatic attendance update on approval

### 💰 Payroll Management
- Comprehensive salary structure
- Allowances (HRA, DA, TA, Medical, etc.)
- Deductions (PF, Tax, Insurance, etc.)
- Automatic gross and net salary calculation
- Salary slip generation
- Month-wise payroll records

### 📊 Reports & Analytics
- Attendance reports
- Leave reports
- Payroll reports
- Department-wise statistics
- Employee overview

### 🔔 Notifications
- In-app notifications
- Leave status updates
- Payroll notifications
- Real-time alerts

### 🎨 Modern UI/UX
- Clean and professional interface
- Responsive design (mobile-friendly)
- Intuitive navigation
- Dashboard with key metrics
- Color-coded status indicators

## 🛠️ Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- SQLite (Database)

**Frontend:**
- HTML5
- CSS3 (Custom styling)
- JavaScript (Vanilla JS)

**Security:**
- Werkzeug password hashing
- Session management
- CSRF protection
- Role-based access control

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```powershell
cd C:\Users\Lenovo\OneDrive\Desktop\hackthon
# Project already exists in: Dayflow-HRMS
```

### 2. Navigate to Project Directory

```powershell
cd Dayflow-HRMS
```

### 3. Create Virtual Environment (Recommended)

```powershell
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 6. Create Sample Data

```powershell
python create_sample_data.py
```

This will create:
- Admin account
- HR officer account
- 20 sample employees
- Attendance records (past 30 days)
- Leave requests
- Payroll records
- Notifications

### 7. Run the Application

```powershell
python run.py
```

The application will start on: **http://localhost:5000**

## 🔑 Default Login Credentials

### Admin Account
- **Email:** admin@dayflow.com
- **Password:** admin123

### HR Officer Account
- **Email:** hr@dayflow.com
- **Password:** hr123

### Employee Account (Sample)
- **Email:** employee1@dayflow.com to employee20@dayflow.com
- **Password:** emp123

## 📁 Project Structure

```
Dayflow-HRMS/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── main.py              # Main routes
│   │   ├── employee.py          # Employee routes
│   │   └── admin.py             # Admin routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   ├── js/
│   │   │   └── main.js          # JavaScript functionality
│   │   └── uploads/             # Profile photos
│   └── templates/
│       ├── base.html            # Base template
│       ├── auth/                # Authentication templates
│       ├── employee/            # Employee templates
│       └── admin/               # Admin templates
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── create_sample_data.py        # Sample data generator
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 📚 User Guide

### For Employees

1. **Dashboard**
   - View attendance summary
   - Quick check-in/check-out
   - Recent leave requests
   - Latest salary information
   - Unread notifications

2. **Profile Management**
   - View personal information
   - Edit contact details
   - Upload profile photo

3. **Attendance**
   - Check-in at start of day
   - Check-out at end of day
   - View attendance history
   - Track present/absent/leave days

4. **Leave Management**
   - Apply for leave
   - Select leave type and dates
   - Provide reason
   - Track leave status
   - View leave history

5. **Payroll**
   - View salary structure
   - Check monthly payslips
   - Download salary slips
   - Track payment history

### For Admin/HR

1. **Dashboard**
   - Overview statistics
   - Today's attendance summary
   - Pending leave requests
   - Department-wise data
   - Recent activities

2. **Employee Management**
   - View all employees
   - Add new employees
   - Edit employee details
   - Manage employee status
   - Search and filter employees

3. **Attendance Management**
   - View all attendance records
   - Mark attendance manually
   - Modify attendance records
   - Filter by date and employee

4. **Leave Management**
   - View all leave requests
   - Approve/reject requests
   - Add admin comments
   - Automatic attendance update

5. **Payroll Management**
   - Create monthly payroll
   - Edit salary structures
   - Process payments
   - Generate salary slips

6. **Reports**
   - Attendance reports
   - Leave reports
   - Payroll reports
   - Export to CSV

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///dayflow.db'

# Security
SECRET_KEY = 'your-secret-key'

# Upload settings
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Pagination
ITEMS_PER_PAGE = 10
```

## 🔒 Security Features

- Passwords are hashed using Werkzeug's security functions
- Session-based authentication with Flask-Login
- CSRF protection enabled
- Role-based access control
- Secure file uploads with validation
- SQL injection prevention through SQLAlchemy ORM

## 🎯 Key Functionalities

### Attendance Workflow
1. Employee checks in at start of day
2. System records check-in time
3. Employee checks out at end of day
4. System calculates working hours
5. Admin can view and modify records

### Leave Approval Workflow
1. Employee applies for leave
2. Request goes to admin/HR
3. Admin reviews and approves/rejects
4. System automatically marks attendance as "Leave" for approved dates
5. Employee receives notification

### Payroll Processing
1. Admin creates payroll for employee
2. System calculates gross salary (Basic + Allowances)
3. System calculates deductions (PF + Tax + Insurance)
4. Net salary = Gross - Deductions
5. Employee receives notification
6. Employee can download salary slip

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🐛 Troubleshooting

### Database Errors
```powershell
# Delete the database and recreate
rm dayflow.db
python create_sample_data.py
```

### Port Already in Use
```powershell
# Run on different port
flask run --port 5001
```

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🚀 Production Deployment

For production deployment:

1. Change `SECRET_KEY` in config.py
2. Use PostgreSQL or MySQL instead of SQLite
3. Set `DEBUG = False`
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Enable HTTPS
6. Set up proper logging
7. Configure backup strategy

## 📝 License

This project is created for educational and hackathon purposes.

## 👥 Support

For issues or questions, please contact the development team.

## 🎉 Features Highlights

✅ Complete CRUD operations for all modules
✅ Role-based dashboards
✅ Real-time notifications
✅ Comprehensive reporting
✅ Clean MVC architecture
✅ Secure authentication
✅ Responsive UI
✅ Production-ready code
✅ Well-documented
✅ Sample data included

---

## 🎊 Hackathon Ready!

This is a **complete, production-grade HRMS** with:
- ✓ All required features implemented
- ✓ Clean, modern UI
- ✓ Secure backend
- ✓ Comprehensive documentation
- ✓ Sample data for demo
- ✓ Easy setup and deployment

**Built with ❤️ for Dayflow HRMS**

*Every workday, perfectly aligned.*
