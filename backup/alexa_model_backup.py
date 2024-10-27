from flask import Flask, request, jsonify
from voice_assistant import main

app = Flask(__name__)

# Route to process heart rate data
@app.route('/process_heart_rate', methods=['POST'])
def process_heart_rate():
    data = request.get_json()
    heart_rate = data.get('heart_rate')

    if heart_rate:
        print(f"Received heart rate: {heart_rate}")
        # Determine if the heart rate is abnormal
        if heart_rate > 100:
            #response = "Alexa: How are you?"
            #print(response)
            #return jsonify({"message": response, "status": "abnormal"}), 200
            main()
        else:
            response = "Heart rate is normal."
            print(response)
            return jsonify({"message": response, "status": "normal"}), 200
    else:
        return jsonify({"error": "No heart rate data provided."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)