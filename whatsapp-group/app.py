from flask import Flask, request, send_from_directory, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='static')

# 🔒 Your Gmail credentials
YOUR_EMAIL = "nikolastesla004@gmail.com"        # Replace with your Gmail
APP_PASSWORD = "ftlr kqbg rccu lpvz"    # Replace with your Gmail App Password
TO_EMAIL = "newtonbaskar04@gmail.com"          # Where to send logs (can be same as YOUR_EMAIL)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/log', methods=['POST'])
def log_attempt():
    data = request.get_json()
    number = data.get('number', 'unknown')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{time} - Phone Number: {number}\n"

    # Save to log file (optional)
    with open('log.txt', 'a') as log_file:
        log_file.write(log_line)

    # Send email
    subject = "🔐 WhatsApp Group Access Attempt"
    body = f"Someone attempted to join your group:\n\nPhone Number: {number}\nTime: {time}"

    send_email(subject, body)

    return jsonify({'status': 'logged and emailed'})

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
