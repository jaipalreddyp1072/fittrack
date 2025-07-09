from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from otp_manager import generate_otp, verify_otp
from werkzeug.security import generate_password_hash, check_password_hash
from database import (
    insert_user, get_user_by_mobile, get_user_by_email,
    insert_body_fat, insert_calorie_log, save_health_parameters, get_connection
)

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CORS(app, supports_credentials=True)

@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

# === OTP via email for signup only ===
@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.json.get('email')
    otp = generate_otp(email)
    return jsonify({"message": "OTP sent to email!"})

@app.route('/verify_signup_otp', methods=['POST'])
def verify_signup_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if verify_otp(email, otp):
        password_hash = generate_password_hash(data['password'])
        user_data = {
            "first_name": data['first_name'],
            "surname": data['surname'],
            "age": data['age'],
            "gender": data['gender'],
            "email": data['email'],
            "mobile": data['mobile'],
            "password_hash": password_hash
        }
        user_id = insert_user(user_data)
        session['logged_in'] = True
        session['user_id'] = user_id
        session['user_name'] = data['first_name']
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"}), 401

# === Password-based login ===
@app.route('/login_password', methods=['POST'])
def login_password():
    data = request.get_json()
    login_id = data.get('login')  # email or phone
    password = data.get('password')

    user = get_user_by_email(login_id) or get_user_by_mobile(login_id)
    if user and check_password_hash(user['password_hash'], password):
        session['logged_in'] = True
        session['user_id'] = user['id']
        session['user_name'] = user['first_name']
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard/<section>')
def dashboard_section(section):
    if not session.get("logged_in"):
        return redirect('/login')
    if section == "fat":
        return render_template("dashboard_fat.html")
    elif section == "calories":
        return render_template("dashboard_calories.html")
    elif section == "health":
        return render_template("dashboard_health.html")
    elif section == "charts":
        return render_template("dashboard_charts.html")
    else:
        return "Section not found", 404

@app.route('/calculate/fat', methods=['POST'])
def calculate_fat():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    try:
        fat = round((float(data['waist']) + float(data['hips']) - float(data['neck'])) / float(data['height']) * 100, 2)
    except:
        fat = round((float(data['waist']) - float(data['neck'])) / float(data['height']) * 100, 2)
    insert_body_fat(session['user_id'], data, fat)
    return jsonify({"fat": fat})

@app.route('/calculate/calories', methods=['POST'])
def calculate_calories():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    steps = int(data['steps'])
    time = float(data['time'])
    speed = round(steps / time, 2)
    fat_percentage = 20  # optional: fetch from latest log
    calories = round((steps * fat_percentage * 0.0005), 2)
    insert_calorie_log(session['user_id'], data, speed, calories)
    return jsonify({"speed": speed, "calories": calories})

@app.route('/save/health', methods=['POST'])
def save_health():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    save_health_parameters(session['user_id'], data)
    return jsonify({"message": "Health info saved"})

@app.route('/dashboard/summary')
def dashboard_summary():
    if not session.get("logged_in"):
        return jsonify({"error": "Not logged in"}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT fat_percentage, created_at FROM body_fat_logs WHERE user_id = %s ORDER BY created_at", (session['user_id'],))
    fat_data = cursor.fetchall()

    cursor.execute("SELECT calories, day FROM calorie_logs WHERE user_id = %s ORDER BY created_at", (session['user_id'],))
    cal_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "fat": {
            "labels": [str(row[1].strftime('%b %d')) for row in fat_data],
            "values": [float(row[0]) for row in fat_data]
        },
        "calories": {
            "labels": [row[1] for row in cal_data],
            "values": [float(row[0]) for row in cal_data]
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

