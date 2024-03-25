from flask import Flask, request, jsonify
import requests
import AccessTokenGen

app = Flask(__name__)

def get_pds_data(access_token, NHS_ID):
    # URL for PDS endpoint
    url = f"https://int.api.service.nhs.uk/personal-demographics/FHIR/R4/Patient/{NHS_ID}"

    # Headers for the first API request
    headers = {
        "authorization": f"Bearer {access_token}",
        "accept": "application/fhir+json",
        "nhsd-session-urid": "555021935107",
        "x-correlation-id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
        "x-request-id": "60E0B220-8136-4CA5-AE46-1D97EF59D068"
    }

    # Fetch API request for the first API call
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response is an error
    data = response.json()
    return data

def get_scr_data(access_token, NHS_ID):
    # URL for the first Summary Care Record API GET request
    first_api_url = f"https://int.api.service.nhs.uk/summary-care-record/FHIR/R4/DocumentReference?patient=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C{NHS_ID}&type=http%3A%2F%2Fsnomed.info%2Fsct%7C196981000000101&_sort=date&_count=1"

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
        second_api_url = f"https://int.api.service.nhs.uk/summary-care-record/FHIR/R4/Bundle?composition.identifier={composition_identifier}&composition.subject%3APatient.identifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C{NHS_ID}"

        # Fetch API request for the second API call
        second_response = requests.get(second_api_url, headers=headers)
        second_response.raise_for_status()  # Raises a HTTPError if the response is an error
        second_data = second_response.json()
        #print("Second API Response:", second_data)
    return second_data

@app.route('/parser?nhs_id=9449305552', methods=['GET'])
def receive_api_request():
    # get access token
    access_token = AccessTokenGen.generate_token()
    # get NHS number
    NHS_ID = request.args.get("nhs_id")
    
    pds_data = get_pds_data(access_token, NHS_ID)
    scr_data = get_scr_data(access_token, NHS_ID)
    combined_json = {
        "patientInfo": pds_data,
        "healthInfo": scr_data
    }
    return jsonify(combined_json)

app.run(debug=True)
