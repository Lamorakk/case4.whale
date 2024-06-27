import base64

import requests
import json
import os
from dotenv import load_dotenv

import encryptor

# Load environment variables from .env file
load_dotenv()
# Retrieve the Bearer token from environment variables
token = os.getenv('BEARER_TOKEN')
if token is None:
    raise ValueError("Bearer token not found. Please set the BEARER_TOKEN environment variable.")

# URL of the API endpoint
url = os.getenv('DATA_URL')
if url is None:
    raise ValueError("Main server url token not found. Please set the DATA_URL environment variable.")


# def get_by_tgid_req(id):
#     # Headers for the request
#     headers = {
#         'Authorization': f'Bearer {token}'
#     }
#     # Send the HTTP GET request with headers
#     response = requests.get(url, headers=headers)
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#
#         # Print the parsed data
#         print(json.dumps(data, indent=4))  # Pretty print the JSON data
#     else:
#         print(f"Failed to retrieve data: {response.status_code}")
#
#
# def post_new_user(id):
#     # URL of the API endpoint
#     salt = os.urandom(16)  # Save this salt for decryption
#     encoded_salt = base64.b64encode(salt).decode('utf-8')
#
#     # Data to be sent in the POST request
#     data = {
#         'login': id,
#         'password': encryptor.execute(id, salt),
#         'salt': encoded_salt,
#     }
#
#     # Headers for the request
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'  # Set the content type to JSON
#     }
#
#     # Send the HTTP POST request with headers and data
#     response = requests.post(url, headers=headers, json=data)
#
#     # Check if the request was successful
#     if response.status_code == 200 or response.status_code == 201:
#         # Parse the JSON response
#         response_data = response.json()
#
#         # Print the parsed data
#         print(json.dumps(response_data, indent=4))  # Pretty print the JSON data
#     else:
#         print(f"Failed to submit data: {response.status_code}")
#         print(response.text)





def get_user_data_by_tgid(tg_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{url}/get_user_by_tgid/{tg_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to get user data: {response.status_code}")


def get_login_token_for_game(tg_id):
    user_data = get_user_data_by_tgid(tg_id)
    return user_data['login'], user_data['password']


