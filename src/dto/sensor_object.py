class SensorObject:
    
    def __init__(self, date, milliseconds, data, sensorObjectType, sensorName):
        self.__date=date
        self.__milliseconds=milliseconds
        self.__data=data
        self.__sensorObjectType=sensorObjectType
        self.__sensorName=sensorName
    
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, date):
        self.__date=date
    
    @property
    def milliseconds(self):
        return self.__milliseconds
    @milliseconds.setter
    def milliseconds(self, milliseconds):
        self.__milliseconds=milliseconds

    @property    
    def data(self):
        return self.__data
    @data.setter
    def data(self, data):
        self.__data=data
        
    @property    
    def sensorObjectType(self):
        return self.__sensorObjectType
    @sensorObjectType.setter
    def sensorObjectType(self, sensorObjectType):
        self.__sensorObjectType=sensorObjectType
            
    @property    
    def sensorName(self):
        return self.__sensorName
    @sensorName.setter
    def sensorName(self, sensorName):
        self.__sensorName=sensorName