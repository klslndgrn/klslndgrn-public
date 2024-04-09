from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def fetch_data_from_api(
    client_id="your_client_id",
    client_secret="your_client_secret",
    authorization_base_url="auth.smaapis.de/oauth2/auth",
    token_url="auth.smaapis.de/oauth2/token",
):

    # Create a session using the BackendApplicationClient,
    # which supports the Authorization Code Grant Flow
    client = BackendApplicationClient(client_id)
    oauth = OAuth2Session(client)

    # Fetch the authorization URL,
    # which will prompt the user to authorize the application
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    # Redirect the user to the authorization URL
    # and handle the authorization response
    print(f"Please go to {authorization_url} and authorize access.")
    redirect_resp = input("Paste the full redirect URL here: ")

    # Parse the authorization response to retrieve the authorization code
    authorization_response = oauth.parse_authorization_response(redirect_resp)
    code = authorization_response["code"]

    # Exchange the authorization code for an access token
    token = oauth.fetch_token(token_url, code, client_id, client_secret)
    print(f"Fetched token: {token}")

    # Use the access token to make requests to the API
    response = oauth.get("https://example.com/api/resource")

    # Handle the API response
    try:
        if response.status_code == 200:
            print("API request successful.")
            print(response.json())
            return response.json()
        else:
            print("API request failed:", response.text)
            print("Status code:", response.status_code)
    except Exception as e:
        print("An error occurred while fetching data:", e)
        return None
