import mysql.connector

DB_CONFIG = {
    'host': '34.93.238.15',
    'user': 'root',
    'password': 'FitTrack#2025@DB',
    'database': 'warrior_database'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_user(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (first_name, surname, age, gender, email, mobile, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['first_name'], data['surname'], data['age'],
        data['gender'], data['email'], data['mobile'], data['password_hash']
    ))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def get_user_by_mobile(mobile):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE mobile = %s", (mobile,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def insert_body_fat(user_id, data, fat):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO body_fat_logs (user_id, age, weight, height, chest, biceps, thighs, waist, hips, calf, fat_percentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data.get('age'), data.get('weight'), data.get('height'),
        data.get('chest'), data.get('biceps'), data.get('thighs'),
        data.get('waist'), data.get('hips'), data.get('calf'),
        fat
    ))
    conn.commit()
    cursor.close()
    conn.close()

def insert_calorie_log(user_id, data, speed, calories):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calorie_logs (user_id, day, steps, time_minutes, speed, calories)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data.get('day'), data.get('steps'), data.get('time'),
        speed, calories
    ))
    conn.commit()
    cursor.close()
    conn.close()

def save_health_parameters(user_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO health_parameters (
            user_id, diabetic, pre_food, post_food,
            hba1c, testosterone, fatty_liver, liver_stage
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data.get('diabetic') == 'yes',
        data.get('pre_food'), data.get('post_food'),
        data.get('hba1c'), data.get('testosterone'),
        data.get('fatty_liver') == 'yes',
        data.get('liver_stage') if data.get('fatty_liver') == 'yes' else None
    ))
    conn.commit()
    cursor.close()
    conn.close()

