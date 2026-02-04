from flask import Flask, send_file, request, jsonify
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Folder to save receipts
RECEIPT_FOLDER = "receipts"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

# Example: generate a sample receipt text file
@app.route("/download-receipt")
def download_receipt():
    file_path = os.path.join(RECEIPT_FOLDER, "receipt.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Smart Self Checkout Receipt\n")
        f.write("===========================\n")
        f.write("Item 1 - ₹50\n")
        f.write("Item 2 - ₹30\n")
        f.write("Total: ₹80\n")

    return send_file(file_path, as_attachment=True)

# Send email with receipt to logged-in user
@app.route("/email-receipt", methods=["POST"])
def email_receipt():
    # Read logged-in user's email from login_data.json
    try:
        with open("static/login_data.json", "r") as f:
            login_data = json.load(f)
            receiver_email = login_data.get("username")
            if not receiver_email:
                return jsonify({"error": "Logged-in user email not found"}), 400
    except Exception:
        return jsonify({"error": "Login data not found"}), 400

    sender_email = "shahinmulla851@gmail.com"
    sender_password = "cpjzalkralnkyxjh"  # Your Gmail app password

    subject = "Your Purchase Receipt"
    body = "Attached is your receipt for the recent purchase."

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach receipt file
    file_path = os.path.join(RECEIPT_FOLDER, "receipt.txt")
    if not os.path.exists(file_path):
        return jsonify({"error": "Receipt file not found"}), 404

    with open(file_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename=receipt.txt",
    )
    msg.attach(part)

    # Send email via SMTP SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return jsonify({"status": "Email sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
