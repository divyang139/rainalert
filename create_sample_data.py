"""
Sample data generator for Dayflow HRMS
Run this script to populate the database with sample data
"""
from datetime import datetime, date, timedelta
import random
from app import create_app, db
from app.models import User, Employee, Attendance, LeaveRequest, Payroll, Notification

def create_sample_data():
    """Create sample data for testing"""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create Admin
        print("Creating admin user...")
        admin_user = User(
            employee_id='ADM-001',
            email='admin@dayflow.com',
            role='Admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.flush()
        
        admin_employee = Employee(
            user_id=admin_user.id,
            first_name='Admin',
            last_name='User',
            phone='+91-9876543210',
            department='Administration',
            designation='System Administrator',
            date_of_joining=date(2024, 1, 1),
            employment_type='Full-time',
            status='Active'
        )
        db.session.add(admin_employee)
        
        # Create HR Officer
        print("Creating HR officer...")
        hr_user = User(
            employee_id='HR-001',
            email='hr@dayflow.com',
            role='HR'
        )
        hr_user.set_password('hr123')
        db.session.add(hr_user)
        db.session.flush()
        
        hr_employee = Employee(
            user_id=hr_user.id,
            first_name='Sarah',
            last_name='Johnson',
            phone='+91-9876543211',
            department='Human Resources',
            designation='HR Manager',
            date_of_joining=date(2024, 1, 15),
            employment_type='Full-time',
            status='Active'
        )
        db.session.add(hr_employee)
        
        # Sample employee data
        departments = ['Engineering', 'Sales', 'Marketing', 'Finance', 'Operations']
        designations = {
            'Engineering': ['Software Engineer', 'Senior Developer', 'Team Lead', 'DevOps Engineer'],
            'Sales': ['Sales Executive', 'Sales Manager', 'Business Development Manager'],
            'Marketing': ['Marketing Executive', 'Content Writer', 'Digital Marketing Manager'],
            'Finance': ['Accountant', 'Financial Analyst', 'Finance Manager'],
            'Operations': ['Operations Executive', 'Operations Manager', 'Logistics Coordinator']
        }
        
        first_names = ['John', 'Emma', 'Michael', 'Sophia', 'James', 'Olivia', 'Robert', 'Ava', 'William', 'Isabella',
                      'David', 'Mia', 'Richard', 'Charlotte', 'Joseph', 'Amelia', 'Thomas', 'Harper', 'Daniel', 'Evelyn']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        # Create 20 sample employees
        print("Creating sample employees...")
        employees = []
        for i in range(20):
            dept = random.choice(departments)
            user = User(
                employee_id=f'EMP-{str(i+1).zfill(3)}',
                email=f'employee{i+1}@dayflow.com',
                role='Employee'
            )
            user.set_password('emp123')
            db.session.add(user)
            db.session.flush()
            
            employee = Employee(
                user_id=user.id,
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                phone=f'+91-98765432{str(i+12)}',
                department=dept,
                designation=random.choice(designations[dept]),
                date_of_birth=date(random.randint(1985, 2000), random.randint(1, 12), random.randint(1, 28)),
                date_of_joining=date(2024, random.randint(1, 12), random.randint(1, 28)),
                employment_type=random.choice(['Full-time', 'Full-time', 'Full-time', 'Part-time']),
                gender=random.choice(['Male', 'Female']),
                address=f'{random.randint(1, 999)} Main Street, City, State - {random.randint(100000, 999999)}',
                status='Active'
            )
            db.session.add(employee)
            employees.append(employee)
        
        db.session.flush()
        
        # Create attendance records for the past 30 days
        print("Creating attendance records...")
        today = date.today()
        for days_ago in range(30):
            attendance_date = today - timedelta(days=days_ago)
            
            # Skip weekends for simplicity
            if attendance_date.weekday() >= 5:
                continue
            
            for employee in employees[:15]:  # Create attendance for first 15 employees
                status = random.choices(
                    ['Present', 'Absent', 'Half-day', 'Leave'],
                    weights=[0.8, 0.05, 0.05, 0.1]
                )[0]
                
                attendance = Attendance(
                    employee_id=employee.id,
                    date=attendance_date,
                    status=status,
                    check_in=datetime.combine(attendance_date, datetime.strptime('09:00', '%H:%M').time()) if status in ['Present', 'Half-day'] else None,
                    check_out=datetime.combine(attendance_date, datetime.strptime('18:00', '%H:%M').time()) if status == 'Present' else None,
                )
                db.session.add(attendance)
        
        # Create leave requests
        print("Creating leave requests...")
        leave_types = ['Sick Leave', 'Casual Leave', 'Annual Leave']
        statuses = ['Pending', 'Approved', 'Rejected']
        
        for employee in employees[:10]:
            for _ in range(random.randint(1, 3)):
                start_date = today + timedelta(days=random.randint(1, 30))
                days = random.randint(1, 5)
                end_date = start_date + timedelta(days=days-1)
                
                leave = LeaveRequest(
                    employee_id=employee.id,
                    leave_type=random.choice(leave_types),
                    start_date=start_date,
                    end_date=end_date,
                    days=days,
                    reason=f'Sample leave request for {days} days',
                    status=random.choice(statuses),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 10))
                )
                
                if leave.status != 'Pending':
                    leave.approved_by = admin_user.id if random.random() > 0.5 else hr_user.id
                    leave.approved_at = datetime.now() - timedelta(days=random.randint(0, 5))
                    leave.admin_comment = 'Approved' if leave.status == 'Approved' else 'Insufficient leave balance'
                
                db.session.add(leave)
        
        # Create payroll records
        print("Creating payroll records...")
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        for employee in employees:
            # Create payroll for last 3 months
            for month_offset in range(3):
                month = current_month - month_offset
                year = current_year
                if month <= 0:
                    month += 12
                    year -= 1
                
                basic_salary = random.randint(30000, 80000)
                
                payroll = Payroll(
                    employee_id=employee.id,
                    month=month,
                    year=year,
                    basic_salary=basic_salary,
                    hra=basic_salary * 0.4,
                    da=basic_salary * 0.1,
                    ta=3000,
                    medical_allowance=2000,
                    other_allowances=1000,
                    pf=basic_salary * 0.12,
                    tax=basic_salary * 0.05,
                    insurance=500,
                    other_deductions=0,
                    status='Processed',
                    payment_date=date(year, month, 28)
                )
                payroll.calculate_totals()
                db.session.add(payroll)
        
        # Create notifications
        print("Creating notifications...")
        for employee in employees[:10]:
            notification = Notification(
                employee_id=employee.id,
                title='Welcome to Dayflow',
                message='Welcome to Dayflow HRMS! Please update your profile information.',
                type='info',
                is_read=random.choice([True, False])
            )
            db.session.add(notification)
        
        # Commit all changes
        print("Committing to database...")
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ Sample data created successfully!")
        print("="*50)
        print("\nLogin Credentials:")
        print("-" * 50)
        print("ADMIN:")
        print("  Email: admin@dayflow.com")
        print("  Password: admin123")
        print("\nHR OFFICER:")
        print("  Email: hr@dayflow.com")
        print("  Password: hr123")
        print("\nEMPLOYEE (Sample):")
        print("  Email: employee1@dayflow.com")
        print("  Password: emp123")
        print("-" * 50)
        print("\nYou can now run the application with: python run.py")
        print("="*50)

if __name__ == '__main__':
    create_sample_data()
