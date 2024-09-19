from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

@app.route('/')
def home():
    return "Welcome to the email service!"  # Root route response

@app.route('/send-email', methods=['POST'])
def send_email():
    # Extract form data from JSON
    data = request.get_json()  # Get JSON data
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    # Debugging: Log the received data
    print("Received data:", name, email, subject, message)

    # Create email content
    email_content = f'''
    Name: {name}
    Email: {email}
    Subject: {subject}
    Message: {message}
    '''

    # Create a SendGrid email message
    msg = Mail(
        from_email=os.getenv('FROM_EMAIL'),
        to_emails=os.getenv('TO_EMAIL'),  # Ensure this is defined in your .env file
        subject=f'Contact Form Submission: {subject}',
        plain_text_content=email_content
    )

    try:
        # Send email using SendGrid API
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(msg)
        return jsonify({'status': 'success', 'message': 'Email sent successfully.'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/test-email', methods=['GET'])
def test_email():
    return jsonify({'status': 'info', 'message': 'Test email endpoint not implemented.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
