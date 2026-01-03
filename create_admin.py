"""
Create initial admin user
"""
from app import create_app, db
from app.models import User, Employee
from datetime import datetime

def create_admin():
    """Create initial admin user"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin already exists
            if User.query.filter_by(role='Admin').first():
                print("Admin user already exists!")
                return
            
            # Create admin user
            admin = User(
                employee_id='ADMIN001',
                email='divyangmakwana68@gmail.com',
                role='Admin',
                is_active=True
            )
            admin.set_password('@Qwertyuiop1')
            db.session.add(admin)
            db.session.flush()
            
            # Create admin employee profile
            admin_employee = Employee(
                user_id=admin.id,
                first_name='Admin',
                last_name='User',
                department='Administration',
                designation='System Administrator',
                date_of_joining=datetime.utcnow().date(),
                status='Active'
            )
            db.session.add(admin_employee)
            db.session.commit()
            
            print("\n✓ Admin user created successfully!")
            print("\nLogin Credentials:")
            print("  Email: divyangmakwana68@gmail.com")
            print("  Password: @Qwertyuiop1")
            print("\n⚠️  Please change the password after first login!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error creating admin: {str(e)}")

if __name__ == '__main__':
    create_admin()
