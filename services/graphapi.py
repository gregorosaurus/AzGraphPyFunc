import os
import requests
import msal

GRAPH_API_SCOPE = ['https://graph.microsoft.com/.default']
GRAPH_URI = 'https://graph.microsoft.com'

class GraphAPI: 
    def __init__(self):
        self.tenantId = os.environ["TenantId"]
        self.clientId = os.environ["ClientId"]
        clientSecret = os.environ["ClientSecret"]
        authority = 'https://login.microsoftonline.com/' + self.tenantId

        self.aadapp =  msal.ConfidentialClientApplication(self.clientId, authority=authority, client_credential = clientSecret)

    def authenticate(self):
        print("Authenticating api")
        self.accessToken = self.aadapp.acquire_token_silent(GRAPH_API_SCOPE, account=None)
        if not self.accessToken:
            self.accessToken = self.aadapp.acquire_token_for_client(scopes=GRAPH_API_SCOPE)
            if self.accessToken['access_token']:
                print('New access token retrieved....')
            else:
                print('Error acquiring authorization token.')
        else:
            print('Token retrieved from MSAL Cache....')
        
    
    def get_users(self):
        print('Retrieving users from api')

        if not self.accessToken:
            raise "No access token available to call api"

        requestHeaders = {'Authorization': 'Bearer ' + self.accessToken['access_token']}
        return requests.get(GRAPH_URI +'/v1.0/users', headers=requestHeaders).json()
