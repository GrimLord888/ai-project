from flask import Flask, request, jsonify
from assistant import run_assistant
from twilio.rest import Client

app = Flask(__name__)

# Twilio setup
account_sid = 'AC4cb381206c6c8e0ba80005e7b38987f9'
auth_token = 'a44f701d94aabfb5a05e097618743def'
twilio_number = '+18508885594'
emergency_contact = '+61405529391'

client = Client(account_sid, auth_token)

def send_warning_message(heart_rate):
    message_body = f"Warning: Heart rate is high at {heart_rate} BPM. Immediate attention needed!"
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=emergency_contact
    )
    print(f"Sent message: {message.sid}")

# Route to process heart rate data
@app.route('/process_heart_rate', methods=['POST'])
def process_heart_rate():
    data = request.get_json()
    heart_rate = data.get('heart_rate')

    if heart_rate:
        print(f"Received heart rate: {heart_rate}")
        # Determine if the heart rate is abnormal
        if heart_rate > 100:
            send_warning_message(heart_rate)
            run_assistant()  # Run the assistant as before
            return jsonify({"message": "Warning message sent", "status": "abnormal"}), 200
        else:
            response = "Heart rate is normal."
            print(response)
            return jsonify({"message": response, "status": "normal"}), 200
    else:
        return jsonify({"error": "No heart rate data provided."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)