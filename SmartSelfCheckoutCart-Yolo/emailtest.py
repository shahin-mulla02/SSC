import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("This is a test receipt email.")
msg['Subject'] = "Test Receipt"
msg['From'] = "shahinmulla851@gmail.com"
msg['To'] = "tasnimmulla18@gmail.com"

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("shahinmulla851@gmail.com", "jgjixpkuejarrwgs")
        smtp.send_message(msg)
    print("Email sent successfully ✅")
except Exception as e:
    print("Email failed ❌", e)
