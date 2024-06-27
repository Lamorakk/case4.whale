# import requests
# import json
# import os
# from dotenv import load_dotenv
#
# import encryptor
# import request_data_server
#
# # Load environment variables from .env file
# load_dotenv()
# # Retrieve the Bearer token from environment variables
# token = os.getenv('BEARER_TOKEN')
# if token is None:
#     raise ValueError("Bearer token not found. Please set the BEARER_TOKEN environment variable.")
#
# # URL of the API endpoint
# url = os.getenv('DATA_URL')
# if url is None:
#     raise ValueError("Main server url token not found. Please set the BEARER_TOKEN environment variable.")
#
#
#
# def get_login_token_for_game(id):
#     data_as_json = request_data_server.get_by_tgid_req(id)
#
#     data = {
#         'login': encryptor.execute(data_as_json["login"], data_as_json["salt"]),
#         'password': data_as_json["password"],
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
