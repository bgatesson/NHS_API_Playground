from flask import Flask, request, jsonify
import call_SCR

app = Flask(__name__)

@app.route('/parse-json', methods=['POST'])
def parse_json():
    # Check if the request contains JSON data
    if request.is_json:
        # Get the JSON data
        json_data = request.get_json()

        # Convert the JSON object to a string
        string_data = str(json_data)

        # Return the string data
        return jsonify({"message": "JSON parsed successfully", "data": string_data}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

app.run(debug=True)
