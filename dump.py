function sendApiRequest() {
    // URL for the first Summary Care Record API GET request
    const firstApiUrl = "https://sandbox.api.service.nhs.uk/summary-care-record/FHIR/R4/DocumentReference?patient=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C9000000009&type=http%3A%2F%2Fsnomed.info%2Fsct%7C196981000000101&_sort=date&_count=1";

    // Headers for the first API request
    const headers = new Headers({
        "accept": "application/fhir+json",
        "nhsd-session-urid": "555021935107",
        "x-correlation-id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
        "x-request-id": "60E0B220-8136-4CA5-AE46-1D97EF59D068"
    });

    // Fetch API request for the first API call
    fetch(firstApiUrl, {
        method: "GET",
        headers: headers
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Handle the first API response data here
        console.log("First API Response:", data);

        // Extract the composition identifier from the first API response
        const compositionIdentifier = data.entry[0]?.resource?.masterIdentifier?.value;

        // URL for the second Summary Care Record API GET request
        const secondApiUrl = `https://sandbox.api.service.nhs.uk/summary-care-record/FHIR/R4/Bundle?composition.identifier=${compositionIdentifier}&composition.subject%3APatient.identifier=https%3A%2F%2Ffhir.nhs.uk%2FId%2Fnhs-number%7C9000000009`;

        // Fetch API request for the second API call
        fetch(secondApiUrl, {
            method: "GET",
            headers: headers
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(secondData => {
            // Handle the second API response data here
            console.log("Second API Response:", secondData);

            // Display the results in the designated area
            document.getElementById("apiResponse").innerHTML = `<p>First API Composition Identifier: ${compositionIdentifier}</p><p>Second API Response: ${JSON.stringify(secondData)}</p>`;
        })
        .catch(error => {
            console.error('Second API Error:', error);
            // Display an error message if the second API call fails
            document.getElementById("apiResponse").innerHTML = `<p>Error: ${error.message}</p>`;
        });
    })
    .catch(error => {
        console.error('First API Error:', error);
        // Display an error message if the first API call fails
        document.getElementById("apiResponse").innerHTML = `<p>Error: ${error.message}</p>`;
    });
}
