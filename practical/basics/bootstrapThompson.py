__author__ = 'tessa'

import pandas as pd
import numpy as np
import random as rd
import statsmodels.api as sm
import itertools
import json
import urllib.request
import time


class BootstrapThompson:

    teamID = None
    teamPW = None
    n_people = None
    n_runIDs = None
    n_interactions = None

    n_training_samples = 5
    n_bootstrap_samples = 50
    max_bootstrap_samples = 100

    prior_alpha = 1.
    prior_beta = 1.
    total_revenue = 0
    total_plays = 0

    RANDOM = False

    def __init__(self, teamID, teamPW, n_runIDs, n_interactions, n_people):
        self.teamID = teamID
        self.teamPW = teamPW
        self.n_people = 20 #n_people
        self.n_runIDs = 10 #n_runIDs
        self.n_interactions = 10000# n_interactions
        #self.create_advertisements_list()
        #self.load_advertisements_list()
        self.training()

    def create_advertisements_list(self):
        header = ['5', '15', '35']
        adtype = ['skyscraper', 'square', 'banner']
        color = ['green']
        productid = ['10']#['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25']
        price = ['10', '20', '30', '40', '50'] #['0', '10', '20', '30', '40', '50']
        advertisements_list = list(itertools.product(header, adtype, color, productid, price))

        advertisements = []
        for i in range(0, len(advertisements_list)):
            advertisement = {'header' : advertisements_list[i]["header"], 'adtype' : advertisements_list[i]["adtype"], 'color' : advertisements_list[i]["color"],
                             'productid' : advertisements_list[i]["productid"], 'price' : advertisements_list[i]["price"]}
            advertisements.append(advertisement)
        print(type(advertisements))
        print(np.shape(advertisements))
        print(advertisements[0:10])

        with open('advertisements3.json', 'a') as file:
            json.dump(advertisements, file)

    def load_advertisements_list(self):
        with open('advertisements.json') as file:
            advertisements = json.load(file)
        print(str(np.shape(advertisements)[0]) + ' advertisements loaded')
        return advertisements

    def advertisement_list_to_booleans(self, advertisement):
        booleans = []
        for i in range(0, 33):
            booleans.append(0)
        if(advertisement["header"] == '5'):
            booleans[0] = 1
        if(advertisement["header"] == '15'):
            booleans[1] = 1
        if(advertisement["header"] == '35'):
            booleans[2] = 1
        if(advertisement["adtype"] == 'skyscraper'):
            booleans[3] = 1
        if(advertisement["adtype"] == 'square'):
            booleans[4] = 1
        if(advertisement["adtype"] == 'banner'):
            booleans[5] = 1
        if(advertisement["color"] == 'green'):
            booleans[6] = 1
        if(advertisement["color"] == 'blue'):
            booleans[7] = 1
        if(advertisement["color"] == 'red'):
            booleans[8] = 1
        if(advertisement["color"] == 'black'):
            booleans[9] = 1
        if(advertisement["color"] == 'white'):
            booleans[10] = 1
        if(advertisement["productid"] == '10'):
            booleans[11] = 1
        if(advertisement["productid"] == '11'):
            booleans[12] = 1
        if(advertisement["productid"] == '12'):
            booleans[13] = 1
        if(advertisement["productid"] == '13'):
            booleans[14] = 1
        if(advertisement["productid"] == '14'):
            booleans[15] = 1
        if(advertisement["productid"] == '15'):
            booleans[16] = 1
        if(advertisement["productid"] == '16'):
            booleans[17] = 1
        if(advertisement["productid"] == '17'):
            booleans[18] = 1
        if(advertisement["productid"] == '18'):
            booleans[19] = 1
        if(advertisement["productid"] == '19'):
            booleans[20] = 1
        if(advertisement["productid"] == '20'):
            booleans[21] = 1
        if(advertisement["productid"] == '21'):
            booleans[22] = 1
        if(advertisement["productid"] == '22'):
            booleans[23] = 1
        if(advertisement["productid"] == '23'):
            booleans[24] = 1
        if(advertisement["productid"] == '24'):
            booleans[25] = 1
        if(advertisement["productid"] == '25'):
            booleans[26] = 1
        if(advertisement["price"] == '0'):
            booleans[27] = 1
        if(advertisement["price"] == '10'):
            booleans[28] = 1
        if(advertisement["price"] == '20'):
            booleans[29] = 1
        if(advertisement["price"] == '30'):
            booleans[30] = 1
        if(advertisement["price"] == '40'):
            booleans[31] = 1
        if(advertisement["price"] == '50'):
            booleans[32] = 1

        return booleans

    def booleans_list_to_advertisements(self, booleans):
        header = None
        adtype = None
        color = None
        productid = None
        price = None
        if(booleans[0] == 1):
            header = '5'
        if(booleans[1] == 1):
            header = '15'
        if(booleans[2] == 1):
            header = '35'
        if(booleans[3] == 1):
            adtype = 'skyscraper'
        if(booleans[4] == 1):
            adtype = 'square'
        if(booleans[5] == 1):
            adtype = 'banner'
        if(booleans[6] == 1):
            color = 'green'
        if(booleans[7] == 1):
            color = 'blue'
        if(booleans[8] == 1):
            color = 'red'
        if(booleans[9] == 1):
            color = 'black'
        if(booleans[10] == 1):
            color = 'white'
        if(booleans[11] == 1):
            productid = '10'
        if(booleans[12] == 1):
            productid = '11'
        if(booleans[13] == 1):
            productid = '12'
        if(booleans[14] == 1):
            productid = '13'
        if(booleans[15] == 1):
            productid = '14'
        if(booleans[16] == 1):
            productid = '15'
        if(booleans[17] == 1):
            productid = '16'
        if(booleans[18] == 1):
            productid = '17'
        if(booleans[19] == 1):
            productid = '18'
        if(booleans[20] == 1):
            productid = '19'
        if(booleans[21] == 1):
            productid = '20'
        if(booleans[22] == 1):
            productid = '21'
        if(booleans[23] == 1):
            productid = '22'
        if(booleans[24] == 1):
            productid = '23'
        if(booleans[25] == 1):
            productid = '24'
        if(booleans[26] == 1):
            productid = '25'
        if(booleans[27] == 1):
            price = '0'
        if(booleans[28] == 1):
            price = '10'
        if(booleans[29] == 1):
            price = '20'
        if(booleans[30] == 1):
            price = '30'
        if(booleans[31] == 1):
            price = '40'
        if(booleans[32] == 1):
            price = '50'
        return header, adtype, color, productid, price

    def context_to_booleans(self, context):
        booleans = []
        for i in range(0, 18):
            booleans.append(0)

        if(context.get('Agent') == "OSX"):
            booleans[0] = 1
        if(context.get('Agent') == "Windows"):
            booleans[1] = 1
        if(context.get('Agent') == "Linux"):
            booleans[2] = 1
        if(context.get('Agent') == "mobile"):
            booleans[3] = 1
        if(context.get('Language') == "EN"):
            booleans[4] = 1
        if(context.get('Language') == "NL"):
            booleans[5] = 1
        if(context.get('Language') == "GE"):
            booleans[6] = 1
        if(context.get('Language') == "NA"):
            booleans[7] = 1
        if(context.get('Age') <= 18):
            booleans[8] = 1
        if(context.get('Age') > 18 and context.get('Age') <= 25):
            booleans[9] = 1
        if(context.get('Age') > 25 and context.get('Age') <= 35):
            booleans[10] = 1
        if(context.get('Age') > 35 and context.get('Age') <= 50):
            booleans[11] = 1
        if(context.get('Age') > 50 and context.get('Age') <= 65):
            booleans[12] = 1
        if(context.get('Age') > 65 and context.get('Age') <= 80):
            booleans[13] = 1
        if(context.get('Age') > 80):
            booleans[14] = 1
        if(context.get('Referer') == 'Bing'):
            booleans[15] = 1
        if(context.get('Referer') == 'Google'):
            booleans[16] = 1
        if(context.get('Referer') == 'NA'):
            booleans[17] = 1
        return booleans

    def training(self):
        print("Running training...")

        print("Initializing arms")

        arms = []
        advertisements = self.load_advertisements_list()

        n_features = 51
        weights = []
        learning_rate = 0.001

        cum_revenue = 0
        n_success = 0


        if(self.RANDOM):
            exploration_phase = self.n_interactions
        else:
            exploration_phase = 1500

        for w in range(0, n_features):
            weights.append(1.)

        for ad in advertisements:
            arms.append(self.advertisement_list_to_booleans(ad))

        for runID in range(1, self.n_runIDs+1):
            print("RunID " + str(runID))
            for i in range(1, self.n_interactions+1):
                if (i % 500 == 0):
                    print("Interaction " + str(i))
                    print("  - Cumulative revenue so far " + str(cum_revenue))
                    print("  - Number of successes " + str(n_success))
                    print("  - Average revenue " + str(cum_revenue/n_success))

                if (i % 5000 == 0):
                    time.sleep(5)
                context = self.getcontext(runID, i)
                context = self.context_to_booleans(context)

                #explore or exploit for arm choice
                if i < exploration_phase:
                    #pick random
                    chosen_arm = rd.randrange(0, len(advertisements), 1)
                else:
                    outcomes = []
                    for arm in arms: #compute best
                        feature_vector = arm + context
                        outcome = np.dot(np.asarray(weights), np.asarray(feature_vector))
                        outcomes.append(outcome)
                    chosen_arm = np.argmax(outcomes)

                ad_h, ad_t, ad_c, ad_pid, ad_price = self.booleans_list_to_advertisements(arms[chosen_arm])

                revenue, success = self.proposepage(runID, i, ad_h, ad_t, ad_c, ad_pid, ad_price)
                if success == 1:
                    cum_revenue = cum_revenue + int(ad_price)
                    n_success += 1

                #update values
                feature_vector = arms[chosen_arm] + context
                update_indices = np.where(np.asarray(feature_vector) == 1)

                for i in range(0, len(update_indices[0])):
                    if success == 1:
                        weights[update_indices[0][i]] = weights[update_indices[0][i]]+(learning_rate * int(ad_price))
                    else:
                        weights[update_indices[0][i]] = weights[update_indices[0][i]]-(learning_rate * (int(ad_price)*0.5))

        np.save('weights.npy', weights)
        print('Total revenue: ' + str(cum_revenue))
        print('Total success: ' + str(n_success))
        print('Average revenue: ' + str(cum_revenue/n_success))

    def testing(self):
        print("Running testing...")

        print("Initializing arms")

        arms = []
        advertisements = self.load_advertisements_list()

        n_features = 51
        weights = np.load('weights.npy')

        cum_revenue = 0
        n_success = 0

        for w in range(0, n_features):
            weights.append(1.)


        for ad in advertisements:
            arms.append(self.advertisement_list_to_booleans(ad))

        for runID in range(1, self.n_runIDs+1):
            print("RunID " + str(runID))

            for i in range(1, self.n_interactions+1):
                if (i % 500 == 0):
                    print("Interaction " + str(i))

                if (i % 5000 == 0):
                    time.sleep(5)
                context = self.getcontext(runID, i)
                context = self.context_to_booleans(context)

                #pick arm to pull
                outcomes = []
                for arm in arms: #compute best
                    feature_vector = arm + context
                    outcome = np.dot(np.asarray(weights), np.asarray(feature_vector))
                    outcomes.append(outcome)
                chosen_arm = np.argmax(outcomes)

                ad_h, ad_t, ad_c, ad_pid, ad_price = self.booleans_list_to_advertisements(arms[chosen_arm])

                revenue, success = self.proposepage(runID, i, ad_h, ad_t, ad_c, ad_pid, ad_price)
                if success == 1:
                    cum_revenue += int(revenue)
                    n_success += 1

        print('Total revenue: ' + str(cum_revenue))
        print('Total success: ' + str(n_success))
        print('Average revenue: ' + str(cum_revenue/n_success))

    def getcontext(self, runID, i):
        res = urllib.request.urlopen("http://krabspin.uci.ru.nl/getcontext.json/?i="+str(i)+"&runid="+str(runID)+"&teamid=" + self.teamID + "&teampw=" + self.teamPW).read()
        obj = json.loads(res.decode())  # Example: {'context': {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}}
        context = obj.get('context')    # Example: {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}
        #age = context.get('Age')        # Example: 42.0
        #agent = context.get('Agent')    # Example: 'mobile'
        #id = context.get('ID')          # Example: 236
        #referer = context.get('Referer')    # Example: 'Bing'
        #language = context.get('Language')  # Example: 'EN'
        return context #obj, context, age, agent, id, referer, language

    def proposepage(self, runID, i, header, adtype, color, productid, price):
        url = 'http://krabspin.uci.ru.nl/proposePage.json/?' + 'i=' + str(i) + '&runid=' + str(runID) + '&teamid=' + self.teamID \
              + '&header=' + header + '&adtype=' + adtype + '&color=' + color + '&productid=' + productid \
              + '&price=' + str(price) + '&teampw=' + self.teamPW
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

        return revenue, success

    def compute_revenue_single_user(self, price, success):
        return price*success