# Internship & Skill Assessment Platform

## 📖 Description

It is a full-stack web application developed using **Flask, HTML, CSS, JavaScript, and SQLite**. The platform is designed to simplify the internship registration and skill assessment process by providing a secure and interactive environment for students.

The application allows users to register, verify their mobile number using an OTP verification system, securely log in, participate in an online assessment, and view their performance. It also provides internship opportunities, certification voucher information, and a responsive user interface for an enhanced user experience.

---

## 🚀 Features

- Student Registration
- OTP Verification (Simulation)
- Secure Login Authentication
- Password Hashing using Werkzeug
- Internship Dashboard
- Online Skill Assessment
- Automatic Score Evaluation
- High Performer Detection
- Discount Coupon & Feedback Link
- SQLite Database Integration
- Responsive User Interface
- Session Management

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- SQLite
- Flask-SQLAlchemy
- Werkzeug

---

## 📂 Project Structure

```
Project/
│
├── app.py
├── internship_platform.db
├── templates/
│   └── frontend.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
```

### Navigate to the Project Directory

```bash
cd your-repository
```

### Install Dependencies

```bash
pip install flask flask_sqlalchemy werkzeug twilio
```

### Run the Application

```bash
python3 app.py
```

The application will start at:

```
http://127.0.0.1:5000
```

---

## ☁️ Deployment on Amazon EC2

1. Launch an Amazon EC2 instance.
2. Configure Security Group (SSH, HTTP, HTTPS, Custom TCP 5000).
3. Connect to the EC2 instance using SSH.
4. Install Python and project dependencies.
5. Copy the project files to the EC2 instance.
6. Run the Flask application using:

```bash
python3 app.py
```

7. Open the application in your browser:

```
http://<EC2-Public-IP>:5000
```

---

## 🗄️ Database

The application uses **SQLite** to store student information.

Main table:

- students

To view the database:

```bash
sqlite3 internship_platform.db
```

List tables:

```sql
.tables
```

View student records:

```sql
SELECT * FROM students;
```

---

## 🔒 Security Features

- Password Hashing
- Session Management
- OTP Verification
- Secure Login
- Database Validation

---

## 📷 Application Workflow

```
Splash Screen
        │
        ▼
Student Registration
        │
        ▼
OTP Verification
        │
        ▼
Login
        │
        ▼
Dashboard
        │
        ▼
Online Assessment
        │
        ▼
Result Evaluation
        │
        ▼
Coupon & Feedback
```

---

## 🎯 Future Enhancements

- Real SMS OTP
- Email Verification
- Admin Dashboard
- AI-Based Candidate Analysis
- Certificate Generation
- Payment Gateway Integration
- Resume Upload
- Live Proctoring
- Student Progress Dashboard

---

## 📄 License

This project is intended for educational and learning purposes.

---

## 👨‍💻 Author

Developed as a Full-Stack Flask Internship Project using Python, HTML, CSS, JavaScript, and SQLite.
