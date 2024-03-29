import requests
import uuid
from time import time
import jwt 

def generate_jwt():
    with open("test-2.pem", "r") as f:
        private_key = f.read()

    claims = {
        "sub": "zRHptMpVqAGGi9Edln535lymLeq5Lzd4",
        "iss": "zRHptMpVqAGGi9Edln535lymLeq5Lzd4",
        "jti": str(uuid.uuid4()),
        "aud": "https://int.api.service.nhs.uk/oauth2/token",
        "exp": int(time()) + 300, # 5mins in the future
    }

    additional_headers = {"kid": "test-2"}

    j = jwt.encode(
        claims, private_key, algorithm="RS512", headers=additional_headers
    )
    return j


def generate_token():

    jwtoken = generate_jwt()
    
    url = "https://int.api.service.nhs.uk/oauth2/token"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": f"{jwtoken}"
    }
    response = requests.post(url, headers=headers, data=data)

    access_token = response.json()["access_token"]

    return access_token
