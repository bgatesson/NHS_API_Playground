from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the incoming JSON data
    data = request.get_json()
    print("Received data:", data)
    
    # Here you can process the data or integrate with your application
    
    # Respond back to the sender that the data was received successfully
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=443)
