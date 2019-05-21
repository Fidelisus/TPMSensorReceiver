import Extracted
from bluepy.btle import Scanner

class BLEScanner:
    """
    Static method extractManufacturerData() Scans for devices
    and returns manufacturer data for every connected sensor specified in TPMSDictionary
    """
    TPMSDictionary = {'80:ea:ca:10:06:7d': 'FrontLeft',
                      '81:ea:ca:20:06:55': 'FrontRight',
                      '82:ea:ca:30:04:0e': 'RearLeft',
                      '83:ea:ca:40:03:2e': 'RearRight'}

    @staticmethod
    def getDataFromBLE():
        devicesDictionary = {}
        scanner = Scanner()
        devices = scanner.scan(1.0)
        for dev in devices:
            #print(dev.addr)
            #print(dev.getScanData())
            if BLEScanner.TPMSDictionary.get(dev.addr, "Not TPMS") != "Not TPMS":                
                devicesDictionary[BLEScanner.TPMSDictionary[dev.addr]] = BLEScanner.extractManufacturerData(dev.getScanData())
        return devicesDictionary

    @staticmethod
    def extractManufacturerData(scanData):
        try:
            if scanData[3][1] == "Manufacturer":
                return scanData[3][2]
            else:
                return ""
        except:
            return ""

