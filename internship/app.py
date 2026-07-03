import os
import random
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# =====================================================================
# 📝 BACKEND LINK CONFIGURATION BLOCK (UPDATE YOUR LINKS HERE)
# =====================================================================
PLATFORM_LINKS = {
    "instagram":        "https://instagram.com/your_company_profile",
    "facebook":         "https://facebook.com/your_company_page",
    "chat_box":         "https://your-chat-box-link-here.com",       # <-- Paste your Chat Box link here!
    "proctor_fallback": "https://your-camera-proctoring-link.com/",
    "reward_feedback":  "https://your-coupon-and-feedback-link.com/"
}
# =====================================================================

# SQLite Database Setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'platform_database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student Profile Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    track_type = db.Column(db.String(100), nullable=False)
    id_card_details = db.Column(db.String(200), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    motivation = db.Column(db.Text, nullable=False)

# Dummy verification question matrix
EVALUATION_QUESTION_SET = [
    {"question": "Which data structure runs on a First-In-First-Out basis?", "options": ["Queue", "Stack", "Tree", "Graph"], "correct": "A"},
    {"question": "What is the average time complexity of a standard quicksort run?", "options": ["O(n)", "O(n log n)", "O(n^2)", "O(1)"], "correct": "B"},
    {"question": "Which SQL keyword isolates unique distinct records?", "options": ["UNIQUE", "DIFFERENT", "DISTINCT", "SEPARATE"], "correct": "C"},
    {"question": "Which of the following is an immutable sequential container type in Python?", "options": ["List", "Dictionary", "Set", "Tuple"], "correct": "D"},
    {"question": "What primary utility does the git command group achieve?", "options": ["Compilation", "Version Management", "Containerization", "Styling"], "correct": "B"},
    {"question": "What port maps standard unencrypted HTTP web server payloads?", "options": ["443", "22", "80", "8080"], "correct": "C"},
    {"question": "Which property describes continuous data security persistence layers?", "options": ["ACID", "BASE", "CRUD", "REST"], "correct": "A"},
    {"question": "What layer handles end-to-end segmentation across the OSI network hierarchy?", "options": ["Physical", "Network", "Transport", "Session"], "correct": "C"},
    {"question": "Which component acts as an entry routing gate inside modern MVC designs?", "options": ["Model", "View", "Controller", "Template"], "correct": "C"},
]

@app.route('/')
def home():
    return render_template('frontend', links=PLATFORM_LINKS)

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    req_data = request.get_json() or {}
    mobile = req_data.get('mobile')
    attempt = req_data.get('attempt', 1)
    
    simulated_otp = str(random.randint(1000, 9999))
    session['active_otp_token'] = simulated_otp
    return jsonify({"status": "sent", "otp_preview": simulated_otp})

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    req_data = request.get_json() or {}
    otp_user = req_data.get('otp')
    if otp_user and otp_user == session.get('active_otp_token'):
        return jsonify({"status": "verified"})
    return jsonify({"status": "error", "message": "Invalid code"}), 400

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    try:
        existing = Student.query.filter_by(email=data.get('email')).first()
        if existing:
            return jsonify({"status": "error", "message": "User exists already"}), 400

        new_student = Student(
            name=data.get('name'),
            email=data.get('email'),
            mobile=data.get('mobile'),
            dob=data.get('dob'),
            college=data.get('college'),
            degree=data.get('degree'),
            branch=data.get('branch'),
            track_type=data.get('domain'),
            id_card_details=data.get('id_card_details'),
            password_hash=generate_password_hash(data.get('password')),
            skills=data.get('skills'),
            motivation=data.get('motivation')
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    student = Student.query.filter_by(email=data.get('email')).first()
    if student and check_password_hash(student.password_hash, data.get('password')):
        session['user_email'] = student.email
        return jsonify({
            "status": "success",
            "student": {
                "name": student.name,
                "email": student.email,
                "track_type": student.track_type
            }
        })
    return jsonify({"status": "denied"}), 401

@app.route('/api/get-proctoring-link', methods=['GET'])
def proctor_link():
    return jsonify({"url": PLATFORM_LINKS["proctor_fallback"]})

@app.route('/api/fetch-exam-questions', methods=['POST'])
def fetch_questions():
    sanitized = [{"question": q["question"], "options": q["options"]} for q in EVALUATION_QUESTION_SET]
    return jsonify({"questions": sanitized})

@app.route('/api/evaluate-results', methods=['POST'])
def evaluate():
    data = request.get_json() or {}
    user_answers = data.get('answers', [])
    score = 0
    
    for i, ans in enumerate(user_answers):
        if i < len(EVALUATION_QUESTION_SET) and ans == EVALUATION_QUESTION_SET[i]["correct"]:
            score += 1
            
    pct = (score / len(EVALUATION_QUESTION_SET)) * 100
    return jsonify({
        "score": score,
        "percentage": int(pct),
        "high_performer": bool(score >= 8)
    })

@app.route('/api/get-incentive-link', methods=['GET'])
def incentive_link():
    return jsonify({"coupon_url": PLATFORM_LINKS["reward_feedback"]})

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"status": "logged_out"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=False)
