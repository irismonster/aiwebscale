__author__ = 'tessa'

import urllib.request
import json
import numpy as np

class RestInteraction:

    teamid = None
    teampw = None

    def __init__(self, teamid, teampw):
        self.teamid = teamid
        self.teampw = teampw

    def loopOverPeople(self, runID, N): # RunID is quite obvious, N is number of people, so the i's
        mean = 0
        squares = 0
        K = 3
        # seed the estimated params
        prior_a = 1. # aka successes
        prior_b = 1. # aka failures
        observed_data = np.zeros((K,2))
        observed_data[:,0] += prior_a # allocating the initial conditions
        observed_data[:,1] += prior_b
        regret = np.zeros(N)

        for i in range(N):
            obj, context, age, agent, id, referer, language = self.getcontext(runID, i)
            header, adtype, color, productid, price = self.whichpage(age, agent, id, referer, language, runID, i)

            # pulling a lever & updating observed_data
            this_choice = np.argmax( np.random.beta(observed_data[:,0], observed_data[:,1]) )
            if(this_choice == 0):
                header = '5'
            else:
                if(this_choice == 1):
                    header = '10'
                else:
                    if(this_choice == 2):
                         header = '15'
                    else:
                        print("NO MATCH")
            succes, error, revenue = self.proposepage(runID, i, header, adtype, color, productid, price)
            # update parameters
            if succes == 1:
                update_ind = 0
            else:
                update_ind = 1

            observed_data[this_choice,update_ind] += 1

            # updated expected regret
            regret[i] = N*price - revenue
            #print(revenue)

            mean = mean + (revenue - mean) / (i+1)
            squares = squares + (revenue - mean) * (revenue - mean)
        cum_regret = np.cumsum(regret)
        print(cum_regret)
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
        price = 20 #0-50
        return header, adtype, color, productid, price

    # Thompson Sampling
    # http://www.economics.uci.edu/~ivan/asmb.874.pdf
    # http://camdp.com/blogs/multi-armed-bandits
    def thompson_sampling(observed_data):
        return np.argmax( np.random.beta(observed_data[:,0], observed_data[:,1]) )

    # the bandit algorithm
    def run_bandit_alg(true_rewards,CTRs_that_generated_data,choice_func):
        num_samples,K = true_rewards.shape
        # seed the estimated params
        prior_a = 1. # aka successes
        prior_b = 1. # aka failures
        observed_data = np.zeros((K,2))
        observed_data[:,0] += prior_a # allocating the initial conditions
        observed_data[:,1] += prior_b
        regret = np.zeros(num_samples)

        for i in range(0,num_samples):
            # pulling a lever & updating observed_data
            this_choice = choice_func(observed_data)

            # update parameters
            if true_rewards[i,this_choice] == 1:
                update_ind = 0
            else:
                update_ind = 1

            observed_data[this_choice,update_ind] += 1

            # updated expected regret
            regret[i] = np.max(CTRs_that_generated_data[i,:]) - CTRs_that_generated_data[i,this_choice]

        cum_regret = np.cumsum(regret)

        return cum_regret

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


