import Extracted

class Parser():
    """
    parse() method takes manufacturer data of device and create object of Extracted class
    and sets values for temperature and pressure
    """

    PRESSURE_STARTING_BIT = 8
    TEMPERATURE_STARTING_BIT = 12
    PURE_TEMPERATURE_TO_CELCIUS = 0.01
    DATA_LENGTH = 36
    INT_32_BIT_LENGTH = 4

    @staticmethod
    def ToInt32FromBigEndian(startingBit, string):
        string = string[startingBit*2:(startingBit + Parser.INT_32_BIT_LENGTH)*2]
        byteArr = bytes.fromhex(string)
       
        return int.from_bytes(byteArr, 'little') 

    @staticmethod
    def parse(dataString):
        if len(dataString) != Parser.DATA_LENGTH:
            return None
        else:
            extracted = Extracted.Extracted()
            extracted.pressureInPa = Parser.ToInt32FromBigEndian(Parser.PRESSURE_STARTING_BIT, dataString)
            extracted.temperatureInCelcius = Parser.ToInt32FromBigEndian(Parser.TEMPERATURE_STARTING_BIT, dataString)*Parser.PURE_TEMPERATURE_TO_CELCIUS
            return extracted



