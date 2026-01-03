"""
Clear all employee data from database
"""
from app import create_app, db
from app.models import User, Employee, PreRegisteredEmployee, Attendance, LeaveRequest, Payroll, Notification, OTP

def clear_database():
    """Clear all employee data"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Clearing all employee data from database...")
            
            # Clear in order due to foreign key constraints
            print("- Deleting Notifications...")
            Notification.query.delete()
            
            print("- Deleting OTP records...")
            OTP.query.delete()
            
            print("- Deleting Payroll records...")
            Payroll.query.delete()
            
            print("- Deleting Leave Requests...")
            LeaveRequest.query.delete()
            
            print("- Deleting Attendance records...")
            Attendance.query.delete()
            
            print("- Deleting Employees...")
            Employee.query.delete()
            
            print("- Deleting Users...")
            User.query.delete()
            
            print("- Deleting Pre-Registered Employees...")
            PreRegisteredEmployee.query.delete()
            
            db.session.commit()
            
            print("\n✓ All employee data cleared successfully!")
            print("✓ Database is now empty and ready for fresh data")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error clearing database: {str(e)}")

if __name__ == '__main__':
    confirm = input("Are you sure you want to delete ALL employee data? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_database()
    else:
        print("Operation cancelled.")
