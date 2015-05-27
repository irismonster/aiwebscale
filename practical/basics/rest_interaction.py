__author__ = 'tessa'

import urllib.request
import json

class RestInteraction:

    def __init__(self):
        return

    def getcontext(self):
        return

    def proposepage(self, ):
        teamid = 'Error_Teamname_not_found'
        teampw = '845ea0b18db9a82bc43c811d740d3177'
        runid = '10'
        i = '3'
        header = '5' #5, 15 or 35
        adtype = 'banner' #skyscraper, square or banner
        color = 'black' #green, blue, red, black, white
        productid = '10' #10-25
        price = '10' #0-50

        url = 'http://krabspin.uci.ru.nl/proposePage.json/?' + 'i=' + i + '&runid=' + runid + '&teamid=' + teamid \
              + '&header=' + header + '&adtype=' + adtype + '&color=' + color + '&productid=' + productid \
              + '&price=' + price + '&teampw=' + teampw
        res = urllib.request.urlopen(url).read()
        obj = json.loads(res.decode())

        success = obj.get('effect').get('Success')
        error = obj.get('effect').get('Error')
        if error != None:
            print('PANIEK!')

        return success, error