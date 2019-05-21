import Extracted
import can
import numpy

class ExtractedDataSender:
    TO_BYTE = 128
    PRESSURE_TO_BARS = 0.00001
    # factor to make it fit into 8 bit int
    PRESSURE_TO_INT8 = 0.0001

    @staticmethod
    def printInCelciusAndBars(extracted):
        print(extracted.pressureInPa*ExtractedDataSender.PRESSURE_TO_BARS)
        print(extracted.temperatureInCelcius)

    @staticmethod
    def printData(extracted):
        for sensor in extracted.items():
            if not sensor[1].temperatureInCelcius == -1000:
                print(sensor[0])
                ExtractedDataSender.printInCelciusAndBars(sensor[1])
    
    @staticmethod
    def extractCANData(sensor):
        data = []
        data.append(numpy.int8(sensor.pressureInPa*ExtractedDataSender.PRESSURE_TO_INT8))
        data.append(numpy.int8(sensor.temperatureInCelcius))
        return data
    
    @staticmethod
    def sendDataByCAN(extracted):
    # send a message
        CANData = []
        CANData += ExtractedDataSender.extractCANData(extracted['FrontLeft'])
        CANData += ExtractedDataSender.extractCANData(extracted['FrontRight'])
        CANData += ExtractedDataSender.extractCANData(extracted['RearLeft'])
        CANData += ExtractedDataSender.extractCANData(extracted['RearRight'])
        print(CANData)
        for i, value in enumerate(CANData):
            CANData[i] += ExtractedDataSender.TO_BYTE
        
    # create a bus instance
        bus = can.Bus(interface='socketcan_ctypes',
                      channel='vcan0')
        
        message = can.Message(arbitration_id=123,
                              is_extended_id=False,
                              data=CANData)

        bus.send(message, timeout=0.2)