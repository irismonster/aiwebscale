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
        self.bootstrap_thompson2()

    def create_advertisements_list(self):
        header = ['5', '15', '35']
        adtype = ['skyscraper', 'square', 'banner']
        color = ['green']
        productid = ['10']#['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25']
        price = [25] #['0', '10', '20', '30', '40', '50']
        advertisements_list = list(itertools.product(header, adtype, color, productid, price))

        advertisements = []
        for i in range(0, len(advertisements_list)):
            advertisement = {'header' : advertisements_list[i]["header"], 'adtype' : advertisements_list[i]["adtype"], 'color' : advertisements_list[i]["color"],
                             'productid' : advertisements_list[i]["productid"], 'price' : advertisements_list[i]["price"]}
            advertisements.append(advertisement)
        print(type(advertisements))
        print(np.shape(advertisements))
        print(advertisements[0:10])

        with open('advertisements2.json', 'a') as file:
            json.dump(advertisements, file)

    def load_advertisements_list(self):
        with open('advertisements.json') as file:
            advertisements = json.load(file)
        print(advertisements[0:10])
        print(np.shape(advertisements))
        return advertisements
        #adtype, header, price, productid, color

    def advertisement_list_to_booleans(self, advertisement):
        booleans = []
        for i in range(0, 33):
            booleans.append(False)
        if(advertisement["header"] == '5'):
            booleans[0] = True
        if(advertisement["header"] == '15'):
            booleans[1] = True
        if(advertisement["header"] == '35'):
            booleans[2] = True
        if(advertisement["adtype"] == 'skyscraper'):
            booleans[3] = True
        if(advertisement["adtype"] == 'square'):
            booleans[4] = True
        if(advertisement["adtype"] == 'banner'):
            booleans[5] = True
        if(advertisement["color"] == 'green'):
            booleans[6] = True
        if(advertisement["color"] == 'blue'):
            booleans[7] = True
        if(advertisement["color"] == 'red'):
            booleans[8] = True
        if(advertisement["color"] == 'black'):
            booleans[9] = True
        if(advertisement["color"] == 'white'):
            booleans[10] = True
        if(advertisement["productid"] == '10'):
            booleans[11] = True
        if(advertisement["productid"] == '11'):
            booleans[12] = True
        if(advertisement["productid"] == '12'):
            booleans[13] = True
        if(advertisement["productid"] == '13'):
            booleans[14] = True
        if(advertisement["productid"] == '14'):
            booleans[15] = True
        if(advertisement["productid"] == '15'):
            booleans[16] = True
        if(advertisement["productid"] == '16'):
            booleans[17] = True
        if(advertisement["productid"] == '17'):
            booleans[18] = True
        if(advertisement["productid"] == '18'):
            booleans[19] = True
        if(advertisement["productid"] == '19'):
            booleans[20] = True
        if(advertisement["productid"] == '20'):
            booleans[21] = True
        if(advertisement["productid"] == '21'):
            booleans[22] = True
        if(advertisement["productid"] == '22'):
            booleans[23] = True
        if(advertisement["productid"] == '23'):
            booleans[24] = True
        if(advertisement["productid"] == '24'):
            booleans[25] = True
        if(advertisement["productid"] == '25'):
            booleans[26] = True
        if(advertisement["price"] == '0'):
            booleans[27] = True
        if(advertisement["price"] == '10'):
            booleans[28] = True
        if(advertisement["price"] == '20'):
            booleans[29] = True
        if(advertisement["price"] == '30'):
            booleans[30] = True
        if(advertisement["price"] == '40'):
            booleans[31] = True
        if(advertisement["price"] == '50'):
            booleans[32] = True

        return booleans

    def booleans_list_to_advertisements(self, booleans):
        header = None
        adtype = None
        color = None
        productid = None
        price = None
        if(booleans[0] == True):
            header = '5'
        if(booleans[1] == True):
            header = '15'
        if(booleans[2] == True):
            header = '35'
        if(booleans[3] == True):
            adtype = 'skyscraper'
        if(booleans[4] == True):
            adtype = 'square'
        if(booleans[5] == True):
            adtype = 'banner'
        if(booleans[6] == True):
            color = 'green'
        if(booleans[7] == True):
            color = 'blue'
        if(booleans[8] == True):
            color = 'red'
        if(booleans[9] == True):
            color = 'black'
        if(booleans[10] == True):
            color = 'white'
        if(booleans[11] == True):
            productid = '10'
        if(booleans[12] == True):
            productid = '11'
        if(booleans[13] == True):
            productid = '12'
        if(booleans[14] == True):
            productid = '13'
        if(booleans[15] == True):
            productid = '14'
        if(booleans[16] == True):
            productid = '15'
        if(booleans[17] == True):
            productid = '16'
        if(booleans[18] == True):
            productid = '17'
        if(booleans[19] == True):
            productid = '18'
        if(booleans[20] == True):
            productid = '19'
        if(booleans[21] == True):
            productid = '20'
        if(booleans[22] == True):
            productid = '21'
        if(booleans[23] == True):
            productid = '22'
        if(booleans[24] == True):
            productid = '23'
        if(booleans[25] == True):
            productid = '24'
        if(booleans[26] == True):
            productid = '25'
        if(booleans[27] == True):
            price = '0'
        if(booleans[28] == True):
            price = '10'
        if(booleans[29] == True):
            price = '20'
        if(booleans[30] == True):
            price = '30'
        if(booleans[31] == True):
            price = '40'
        if(booleans[32] == True):
            price = '50'
        return header, adtype, color, productid, price

    def context_to_booleans(self, context):
        booleans = []
        for i in range(0, 18):
            booleans.append(True)

        if(context.get('Agent') == "OSX"):
            booleans[0] = True
        if(context.get('Agent') == "Windows"):
            booleans[1] = True
        if(context.get('Agent') == "Linux"):
            booleans[2] = True
        if(context.get('Agent') == "Mobile"):
            booleans[3] = True
        if(context.get('Language') == "EN"):
            booleans[4] = True
        if(context.get('Language') == "NL"):
            booleans[5] = True
        if(context.get('Language') == "GE"):
            booleans[6] = True
        if(context.get('Language') == "NA"):
            booleans[7] = True
        if(context.get('Age') <= 18):
            booleans[8] = True
        if(context.get('Age') > 18 and context.get('Age') <= 25):
            booleans[9] = True
        if(context.get('Age') > 25 and context.get('Age') <= 35):
            booleans[10] = True
        if(context.get('Age') > 35 and context.get('Age') <= 50):
            booleans[11] = True
        if(context.get('Age') > 50 and context.get('Age') <= 65):
            booleans[12] = True
        if(context.get('Age') > 65 and context.get('Age') <= 80):
            booleans[13] = True
        if(context.get('Age') > 80):
            booleans[14] = True
        if(context.get('referer') == 'Bing'):
            booleans[15] = True
        if(context.get('referer') == 'Google'):
            booleans[16] = True
        if(context.get('referer') == 'NA'):
            booleans[17] = True
        return booleans

    def bootstrap_thompson2(self):
        print("Running bootstrap thompson sampling...")

        print("Initializing arms")

        arms = []
        advertisements = self.load_advertisements_list()

        n_features = 51
        weights = []
        feature_counter = []
        learning_rate = 0.001

        cum_revenue = 0
        n_success = 0




        if(self.RANDOM):
            exploration_phase = self.n_interactions
        else:
            exploration_phase = 500

        for w in range(0, n_features):
            weights.append(1.)


        for i in range(0, 50):
            feature_counter.append(0)

        for ad in advertisements:
            arms.append(self.advertisement_list_to_booleans(ad))

        for runID in range(1, self.n_runIDs+1):
            print("Bliep " + str(runID))
            for i in range(1, self.n_interactions+1):
                if (i % 500 == 0):
                    print("Boop " + str(i))

                if (i % 5000 == 0):
                    time.sleep(5)
                context = self.getcontext(runID, i)
                #print(context)
                context = self.context_to_booleans(context)

                #explore or exploit for arm choice
                chosen_arm = None
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
                    cum_revenue += int(revenue)
                    n_success += 1

                #update values
                feature_vector = arms[chosen_arm] + context
                update_indices = np.where(feature_vector == True)
                update = rd.randrange(0, 1, 1)
                if update == 1:
                    for i in range(0, len(update_indices)):
                        if success == 1:
                            weights[update_indices[i]] = weights[update_indices[i]]*learning_rate
                        else:
                            weights[update_indices[i]] = weights[update_indices[i]]*learning_rate*-1.0


        print('Total revenue: ' + str(cum_revenue))
        print('Total success: ' + str(n_success))
        print('Average revenue: ' + str(cum_revenue/n_success))







        #Initialize priors for alpha and beta

        #for all runIDs
        #for all arms
            #sample j_i from uniform 1...J bootstrap replicates
            #retrieve alpha and beta corresponding
        #play best arm
        #for j ... J do:
            # sample d_j from Bernouilli(1/2)
            # if d_j == 1 then:
                #alpha_ij = alpha_ij + r_t      (r_t = succesrate)
                #beta_ij = beta_ij + (1-r_t)


    def bootstrap_thompson(self):
        print("Running bootstrap thompson sampling...")

        for runID in range(1, self.n_runIDs): #{1,10000}

            print("     Loading advertisements")
            advertisements = self.load_advertisements_list()

            print("     Initializing arms")

            arms = []
            for a in range(0, len(advertisements)):
                arm = {
                    "mean" : 0.5,
                    "advertisement" : advertisements[a],
                    "models" : []
                }
                arms.append(arm)

            #Initialize the alpha and betas for the beta distributions
            #beta_distribution_values = []
            #for a in range(0, len(arms)):
            #    beta_values = (self.prior_alpha, self.prior_beta)
            #    beta_distribution_values.append(beta_values)

            #models&pulls
            for a in range(0, len(arms)):
                arms[a]["pulls"] = 0
                for j in range(0, self.max_bootstrap_samples):
                    arms[a]["models"].append({"model" : None, "df" : pd.DataFrame(), "update" : True})

            print("    Looping i's")
            for i in range(1, self.n_interactions):
                #get visitor info/context
                obj, context, age, agent, id, referer, language = self.getcontext(runID, i)

                visitor_representation = {
                    "agent-OSX" : int(agent == "OSX"),
                    "agent-Windows" : int(agent == "Windows"),
                    "agent-Linux" : int(agent == "Linux"),
                    "agent-Mobile" : int(agent == "Mobile"),
                    "language-EN" : int(language == "EN"),
                    "language-NL" : int(language == "NL"),
                    "language-GE" : int(language == "GE"),
                    "language-NA" : int(language == "NA"),
                    "age-10-18" : int(age <= 18),
                    "age-18-25" : int(age > 18 and age <= 25),
                    "age-25-35" : int(age > 25 and age <= 35),
                    "age-35-50" : int(age > 35 and age <= 50),
                    "age-50-65" : int(age > 50 and age <= 65),
                    "age-65-80" : int(age > 65 and age <= 80),
                    "age-80-110" : int(age > 80 and age <= 110),
                    "referer-Bing" : int(referer == "Bing"),
                    "referer-Google" : int(referer == "Google"),
                    "referer-NA" : int(referer == "NA")
                }

                #predict success rate / conversion
                outcomes = []
                for a in range(0, len(arms)):
                    j = rd.randint(0, self.n_bootstrap_samples-1)

                    if (len(arms[a]["models"][j]["df"]) < self.n_training_samples):
                        outcomes.append(np.random.ranf())
                    else:
                        if (arms[a]["models"][j]["update"] == True):
                            df = arms[a]["models"][j]["df"]
                            print(df)
                            arms[a]["models"][j]["model"] = sm.Logit(df["c"], df[df.columns[1:]]).fit(disp=0)
                            arms[a]["models"][j]["update"] = False
                        outcomes.append(arms[a]["models"][j]["model"].predict(pd.DataFrame([visitor_representation]))[0])

                #predict best advertisement
                arm = np.argmax(outcomes)

                #play that best arm
                revenue, success = self.proposepage(runID, i, arms[arm]["advertisement"]["header"], arms[arm]["advertisement"]["adtype"], arms[arm]["advertisement"]["color"], arms[arm]["advertisement"]["productid"], arms[arm]["advertisement"]["price"])
                arms[arm]["pulls"] += 1
                self.total_plays += 1
                self.total_revenue += 1
                visitor_representation["succes_rate"] = success
                print(visitor_representation["succes_rate"])
                #if visitor_representation["succes_rate"] == 1:
                #    outcomes += 1

                print("    Update bootstrap samples")
                #update bootstrap samples for all pools
                for j in range(0, self.n_bootstrap_samples):
                    if (rd.randint(0, 1) == 1):
                        if arms[arm]["models"][j]["df"] is None:
                            arms[arm]["models"][j]["df"] is pd.DataFrame([visitor_representation])
                        else:
                            if (len(arms[arm]["models"][j]["df"]) == self.max_bootstrap_samples):
                                b = rd.randint(0, self.max_bootstrap_samples-1)
                                arms[arm]["models"][j]["df"][b:b+1] = pd.DataFrame([visitor_representation])
                            else:
                                arms[arm]["models"][j]["df"] = arms[arm]["models"][j]["df"].append(pd.DataFrame([visitor_representation]))
                        if (len(arms[arm]["models"][j]["df"]) >= self.n_training_samples):
                            arms[arm]["models"][j]["update"] = True

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