import Extracted
import Parser
import time
import ExtractedDataSender as Sender
import BLEScanner
import collections

def main():
    ValuesDictionary = {'FrontLeft': Extracted.Extracted(),
                      'FrontRight': Extracted.Extracted(),
                      'RearLeft': Extracted.Extracted(),
                      'RearRight': Extracted.Extracted()}
  
    SEND_INTERVAL = 3
    sendNow = False
    sendInterval = 0
    previous = ValuesDictionary
    
    while(1):
        manufacturerDataDictionary = BLEScanner.BLEScanner.getDataFromBLE()
        print(manufacturerDataDictionary)

        #manufacturerDataDictionary = {'FrontLeft': '83eaca40032e38050000880b00004201'}
                                     # 000181eaca200655f4070000e90900002f01'
        for sensor in manufacturerDataDictionary.items():
            extracted = Parser.Parser.parse(sensor[1])
            
            if Sender.ExtractedDataSender.extractCANData(extracted) !=\
               Sender.ExtractedDataSender.extractCANData(previous[sensor[0]])\
               and not extracted is None:
                ValuesDictionary[sensor[0]] = extracted
                sendNow = True
            previous[sensor[0]] = extracted
            
        #ExtractedDataSender.ExtractedDataSender.printData(ValuesDictionary)
        if sendInterval > SEND_INTERVAL or sendNow:
            Sender.ExtractedDataSender.sendDataByCAN(ValuesDictionary)
            sendNow = False
            sendInterval = 0
        else:
            sendInterval += 1
main()
