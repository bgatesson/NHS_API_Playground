import requests

def send_api_request():
    # URL for the first Summary Care Record API GET request
    first_api_url = "https://sandbox.api.service.nhs.uk/summary-care-record/FHIR/R4/DocumentReference?patient=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C9000000009&type=http%3A%2F%2Fsnomed.info%2Fsct%7C196981000000101&_sort=date&_count=1"

    # Headers for the first API request
    headers = {
        "accept": "application/fhir+json",
        "nhsd-session-urid": "555021935107",
        "x-correlation-id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
        "x-request-id": "60E0B220-8136-4CA5-AE46-1D97EF59D068"
    }

    # Fetch API request for the first API call
    response = requests.get(first_api_url, headers=headers)
    response.raise_for_status()  # Raises a HTTPError if the response is an error
    data = response.json()
    print("First API Response:", data)

    # Extract the composition identifier from the first API response
    composition_identifier = data.get('entry', [{}])[0].get('resource', {}).get('masterIdentifier', {}).get('value')

    if composition_identifier:
        # URL for the second Summary Care Record API GET request
        second_api_url = f"https://sandbox.api.service.nhs.uk/summary-care-record/FHIR/R4/Bundle?composition.identifier={composition_identifier}&composition.subject%3APatient.identifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C9000000009"

        # Fetch API request for the second API call
        second_response = requests.get(second_api_url, headers=headers)
        second_response.raise_for_status()  # Raises a HTTPError if the response is an error
        second_data = second_response.json()
        print("Second API Response:", second_data)