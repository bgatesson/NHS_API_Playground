from flask import Flask, request, jsonify
import requests
import AccessTokenGen

app = Flask(__name__)

@app.route('/parser', methods=['GET'])
def send_api_request():
    # NHS Number
    NHS_number = request.args.get("nhs_id")
    # get access token
    access_token = AccessTokenGen.generate_token()
    print(access_token)
    # URL for the first Summary Care Record API GET request
    first_api_url = f"https://int.api.service.nhs.uk/summary-care-record/FHIR/R4/DocumentReference?patient=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C{NHS_number}&type=http%3A%2F%2Fsnomed.info%2Fsct%7C196981000000101&_sort=date&_count=1"

    # Headers for the first API request
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/fhir+json",
        "nhsd-session-urid": "555021935107",
        "x-correlation-id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
        "x-request-id": "60E0B220-8136-4CA5-AE46-1D97EF59D068"
    }

    # Fetch API request for the first API call
    response = requests.get(first_api_url, headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response is an error
    data = response.json()
    #print("First API Response:", data)

    # Extract the composition identifier from the first API response
    composition_identifier = data.get('entry', [{}])[0].get('resource', {}).get('masterIdentifier', {}).get('value')

    if composition_identifier:
        # URL for the second Summary Care Record API GET request
        second_api_url = f"https://int.api.service.nhs.uk/summary-care-record/FHIR/R4/Bundle?composition.identifier={composition_identifier}&composition.subject%3APatient.identifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C{NHS_number}"

        # Fetch API request for the second API call
        second_response = requests.get(second_api_url, headers=headers)
        second_response.raise_for_status()  # Raises a HTTPError if the response is an error
        second_data = second_response.json()
        #print("Second API Response:", second_data)
    return second_data
    
def receive_api_request():
    data = send_api_request()
    return jsonify(data)

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
