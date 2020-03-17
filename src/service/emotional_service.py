from interface import EmotionalInterface
from dto import SecuritySensorData
from service.security_service import SecurityService

@EmotionalInterface.register
class EmotionalService:
    
    def __init__(self):
        self.__securityService = SecurityService()
    
    #Function to get the emotional state
    def getEmotionalState(self, securitySensorData):
        
        #The sensor data must be instance of security sensor data
        if isinstance(securitySensorData, SecuritySensorData) and self.__securityService.login(securitySensorData.user, securitySensorData.password):
            #TODO: Query the model
            return True
        else:
            return False