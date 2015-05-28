__author__ = 'tessa'

import urllib.request
import json

class RestInteraction:

    def __init__(self):
        return

    def loopOverPeople(self, runID, N): # RunID is quite obvious, N is number of people, so the i's
        for i in range(N):
            self.getcontext(runID, i)
        return

    def getcontext(self, runID, i):
        res = urllib.request.urlopen("http://krabspin.uci.ru.nl/getcontext.json/?i="+str(i)+"&runid="+str(runID)+"&teamid=Error_Teamname_not_found&teampw=845ea0b18db9a82bc43c811d740d3177").read()
        obj = json.loads(res.decode())  # Example: {'context': {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}}
        context = obj.get('context')    # Example: {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}
        age = context.get('Age')        # Example: 42.0
        agent = context.get('Agent')    # Example: 'mobile'
        id = context.get('ID')          # Example: 236
        referer = context.get('Referer')    # Example: 'Bing'
        language = context.get('Language')  # Example: 'EN'
        return obj, context, age, agent, id, referer, language


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

