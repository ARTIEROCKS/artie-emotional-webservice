import config, requests

class SecurityService:
    
    #Function to query if the username and password are correct
    def login(self, user, password):
        url= config.general['API_GATEWAY_PROTOCOL'] + "://" + config.general['API_GATEWAY_HOST'] + ":" + config.general['API_GATEWAY_PORT'] + "/api/v1/users/login?userName=" + user + "&password=" + password
        
        response = requests.get(url)
        return response