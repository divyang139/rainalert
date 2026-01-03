# 🚀 QUICKSTART GUIDE - Dayflow HRMS

## ⚡ Super Quick Setup (5 minutes)

### Step 1: Open PowerShell in Project Directory
```powershell
cd C:\Users\Lenovo\OneDrive\Desktop\hackthon\Dayflow-HRMS
```

### Step 2: Run Setup Script
```powershell
.\setup.ps1
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create database with sample data
- ✅ Set up admin and employee accounts

### Step 3: Start the Application
```powershell
.\start.ps1
```

Or manually:
```powershell
.\venv\Scripts\Activate.ps1
python run.py
```

### Step 4: Open in Browser
Navigate to: **http://localhost:5000**

---

## 🔑 LOGIN CREDENTIALS

### 👨‍💼 Admin Account
- **Email:** admin@dayflow.com
- **Password:** admin123
- **Access:** Full system access, employee management, reports

### 👔 HR Officer Account
- **Email:** hr@dayflow.com
- **Password:** hr123
- **Access:** Employee management, attendance, leave approval, payroll

### 👤 Employee Accounts
- **Email:** employee1@dayflow.com to employee20@dayflow.com
- **Password:** emp123
- **Access:** Personal dashboard, attendance, leave, payroll viewing

---

## 📋 WHAT'S INCLUDED

### Sample Data Created:
- ✅ 1 Admin user
- ✅ 1 HR officer
- ✅ 20 Sample employees
- ✅ 30 days of attendance records
- ✅ Multiple leave requests
- ✅ 3 months of payroll data
- ✅ System notifications

---

## 🎯 QUICK TEST FLOW

### As Employee (employee1@dayflow.com):
1. Login → Dashboard
2. Click "Check In" → Mark attendance
3. Go to Leave → Apply for leave
4. View Payroll → See salary slips
5. Check Profile → Update information

### As Admin (admin@dayflow.com):
1. Login → Admin Dashboard
2. View Employees → See all staff
3. Check Leave Requests → Approve/Reject leaves
4. Mark Attendance → Manually update attendance
5. Create Payroll → Process monthly salaries
6. View Reports → Generate analytics

---

## 🔧 COMMON COMMANDS

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Run Application
```powershell
python run.py
```

### Recreate Database
```powershell
python create_sample_data.py
```

### Install New Package
```powershell
pip install package_name
pip freeze > requirements.txt
```

---

## 📱 FEATURES TO DEMO

### 1. Authentication ✓
- User registration
- Secure login/logout
- Role-based access

### 2. Employee Dashboard ✓
- Attendance summary
- Leave status
- Payroll info
- Notifications

### 3. Attendance Management ✓
- Check-in/Check-out
- View history
- Admin can mark attendance

### 4. Leave Management ✓
- Apply for leave
- Track status
- Admin approval workflow
- Auto-update attendance

### 5. Payroll System ✓
- View salary structure
- Download salary slips
- Admin can process payroll

### 6. Admin Features ✓
- Employee management
- Attendance tracking
- Leave approval
- Payroll processing
- Comprehensive reports

---

## 🎨 UI HIGHLIGHTS

- ✨ Clean, modern design
- 📱 Fully responsive
- 🎯 Intuitive navigation
- 📊 Dashboard with statistics
- 🎨 Color-coded status indicators
- 🔔 Real-time notifications

---

## 🐛 TROUBLESHOOTING

### Issue: "python not found"
**Solution:** Install Python 3.8+ from python.org

### Issue: "Cannot activate venv"
**Solution:** Run in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Port 5000 already in use"
**Solution:** Change port in run.py or kill the process:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Database error
**Solution:** Delete database and recreate:
```powershell
Remove-Item dayflow.db
python create_sample_data.py
```

---

## 📚 PROJECT STRUCTURE

```
Dayflow-HRMS/
├── app/
│   ├── models.py           # Database models
│   ├── routes/             # All route handlers
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, uploads
├── config.py               # Configuration
├── run.py                  # App entry point
├── setup.ps1               # Setup script
├── start.ps1               # Start script
└── README.md               # Full documentation
```

---

## 🎉 DEMO CHECKLIST

For your hackathon presentation, demo these features:

- [ ] Login as Employee
- [ ] Check-in/Check-out attendance
- [ ] Apply for leave
- [ ] View salary slip
- [ ] Login as Admin
- [ ] Approve/Reject leave request
- [ ] Mark attendance for employee
- [ ] Create payroll
- [ ] Generate reports
- [ ] Show responsive design on mobile

---

## 🏆 PRODUCTION-READY FEATURES

✅ Complete MVC architecture
✅ Secure authentication
✅ Role-based access control
✅ Database ORM with SQLAlchemy
✅ Form validation
✅ Error handling
✅ Session management
✅ File upload handling
✅ Responsive design
✅ Clean, documented code

---

## 📞 NEED HELP?

Check the full README.md for:
- Detailed feature documentation
- API documentation
- Deployment guide
- Configuration options
- Security best practices

---

## 🎊 YOU'RE READY!

Your complete HRMS is ready to run. Just execute:

```powershell
.\start.ps1
```

Then open **http://localhost:5000** and start exploring!

**Good luck with your hackathon! 🚀**

---

*Dayflow HRMS - Every workday, perfectly aligned.*
