from .sensor_object import SensorObject

class SecuritySensorData:
    
    def __init__(self, user, password, data):
        self.__user=user
        self.__password=password
        self.__data=data
    
    @property
    def user(self):
        return self.__user
    @user.setter
    def user(self, user):
        self.__user=user
    
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, password):
        self.__password=password

    @property    
    def data(self):
        return self.__data
    @data.setter
    def data(self, data):
        self.__data=data
    