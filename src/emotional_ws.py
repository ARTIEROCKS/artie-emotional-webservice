import flask, json
from service import EmotionalService
from dto import SecuritySensorData

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

#Creating the emotional service
emotionalService = EmotionalService()

@app.route('/api/v1/emotion/getEmotionalState', methods=['POST'])
def getEmotionalState():
    
    #Gets the data from the post request
    json_data = get_data(request.data)
    
    #Transforms into security sensor data object
    securitySensorData = securitySensorData(json_data["user"],
                                            json_data["password"],
                                            json_data["data"])
    
    #Sends the security sensor data to the emotional service
    return emotionalService.getEmotionalState(securitySensorData)


#Function to transform a string to a json
def get_data(data):
    json_data = json.loads(data)
    print("Deserialized data: {}".format(data))
    return json_data


app.run()
