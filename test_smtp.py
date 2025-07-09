import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "SMTP Test"
msg["From"] = "jaiever143@gmail.com"
msg["To"] = "jaipalreddypothireddy23@gmail.com"
msg.set_content("This is a test email from FitTrack OTP")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("jaiever143@gmail.com", "qaqq rsaf ixiy ukkk")
    smtp.send_message(msg)

print("✅ Test Email Sent")

