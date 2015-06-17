__author__ = 'tessa'

import urllib.request
import json

class RestInteraction:

    teamid = None
    teampw = None

    def __init__(self, teamid, teampw):
        self.teamid = teamid
        self.teampw = teampw

    def loopOverPeople(self, runID, N): # RunID is quite obvious, N is number of people, so the i's
        mean = 0
        squares = 0
        for i in range(N):
            obj, context, age, agent, id, referer, language = self.getcontext(runID, i)
            header, adtype, color, productid, price = self.whichpage(age, agent, id, referer, language, runID, i)
            succes, error, revenue = self.proposepage(runID, i, header, adtype, color, productid, price)
            mean = mean + (revenue - mean) / (i+1)
            squares = squares + (revenue - mean) * (revenue - mean)
        variance = squares / (i + 1)
        print(mean)
        print(variance)
        return mean, variance

    def getcontext(self, runID, i):
        res = urllib.request.urlopen("http://krabspin.uci.ru.nl/getcontext.json/?i="+str(i)+"&runid="+str(runID)+"&teamid=" + self.teamid + "&teampw=" + self.teampw).read()
        obj = json.loads(res.decode())  # Example: {'context': {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}}
        context = obj.get('context')    # Example: {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}
        age = context.get('Age')        # Example: 42.0
        agent = context.get('Agent')    # Example: 'mobile'
        id = context.get('ID')          # Example: 236
        referer = context.get('Referer')    # Example: 'Bing'
        language = context.get('Language')  # Example: 'EN'
        return obj, context, age, agent, id, referer, language

    def whichpage(self, age, agent, id, referer, language, runID, i):
        header = '5' #5, 15 or 35
        adtype = 'skyscraper' #skyscraper, square or banner
        color = 'green' #green, blue, red, black, white
        productid = '10' #10-25
        price = 1 #0-50
        return header, adtype, color, productid, price

    def proposepage(self, runID, i, header, adtype, color, productid, price):
        url = 'http://krabspin.uci.ru.nl/proposePage.json/?' + 'i=' + str(i) + '&runid=' + str(runID) + '&teamid=' + self.teamid \
              + '&header=' + header + '&adtype=' + adtype + '&color=' + color + '&productid=' + productid \
              + '&price=' + str(price) + '&teampw=' + self.teampw
        res = urllib.request.urlopen(url).read()
        obj = json.loads(res.decode())

        success = obj.get('effect').get('Success')
        error = obj.get('effect').get('Error')
        if error != None:
            print('!!! An error was given in the propose page function !!!')
            return

        revenue = self.compute_revenue_single_user(price, success)
        #print('You asked ' + str(price) + ' euro.')
        #print('Your revenue was: ' + str(revenue))

        return success, error, revenue

    def compute_revenue_single_user(self, price, success):
        return price*success


