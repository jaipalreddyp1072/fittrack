import smtplib
import random
import time
from email.message import EmailMessage

# In-memory OTP store
otp_storage = {}

# ✅ Your Gmail credentials (App Password recommended)
SMTP_EMAIL = "jaiever143@gmail.com"               # 🔁 Replace this
SMTP_PASSWORD = "qaqq rsaf ixiy ukkk"         # 🔁 Replace this (App password only)

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {
        "otp": otp,
        "timestamp": time.time()
    }

    msg = EmailMessage()
    msg["Subject"] = "FitTrack Signup OTP"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email
    msg.set_content(f"Hi, welcome to FitTrack!\n\nYour OTP is: {otp}\nIt is valid for 5 minutes.\n\nPlease do not share it.")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"[EMAIL OTP] Sent to {email}: {otp}")
    except Exception as e:
        print("[EMAIL OTP ERROR]:", e)

    return otp

def verify_otp(email, otp_input):
    record = otp_storage.get(email)
    if not record:
        return False
    if time.time() - record["timestamp"] > 300:  # OTP expired
        del otp_storage[email]
        return False
    if record["otp"] == otp_input:
        del otp_storage[email]
        return True
    return False

