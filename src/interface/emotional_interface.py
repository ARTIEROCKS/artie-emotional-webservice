import abc

class EmotionalInterface(abc.ABC):
    
    @abc.abstractmethod
    def getEmotionalState(self, sensorData):
        pass