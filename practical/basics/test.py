__author__ = 'tessa'

import pandas as pd
import numpy as np
import random as rd
import statsmodels.api as sm
import itertools
import json
import urllib.request
from math import exp, log, sqrt


class Test:

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

    alpha = .1

    def __init__(self, teamID, teamPW, n_runIDs, n_interactions, n_people):
        self.teamID = teamID
        self.teamPW = teamPW
        self.n_people = 20 #n_people
        self.n_runIDs = 3 #n_runIDs
        self.n_interactions = n_interactions
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
        with open('advertisements2.json') as file:
            advertisements = json.load(file)
        print(advertisements[0:10])
        print(np.shape(advertisements))
        return advertisements
        #adtype, header, price, productid, color

    def get_probability_estimation(self, features, weights):
        wTx = 0
        for feat in features:
            wTx += weights[feat] * 1.
        return 1. / (1. + exp(-max(min(wTx, 20.), -20.))) # sigmoid

    def update_w (self, weights, feature_counter, feature, model_prediction, result):
        for i in feature:
            weights[i] -= (model_prediction-result) * self.alpha / (sqrt(feature_counter[i]) + 1.)
            feature_counter[i] += 1.
        return weights, feature_counter

    weights = []
    feature_counter = []



    def algorithm(self):
        self.weights = [1.] ** 50       #Initialize weights for linear regression


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
        for runID in range(0, self.n_runIDs):
            for i in range(0, self.n_interactions):

                obj, context, age, agent, id, referer, language = self.getcontext(runID, i)

                features =
                prediction = self.get_probability_estimation()


    def getcontext(self, runID, i):
        res = urllib.request.urlopen("http://krabspin.uci.ru.nl/getcontext.json/?i="+str(i)+"&runid="+str(runID)+"&teamid=" + self.teamID + "&teampw=" + self.teamPW).read()
        obj = json.loads(res.decode())  # Example: {'context': {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}}
        context = obj.get('context')    # Example: {'ID': 236, 'Age': 42.0, 'Agent': 'mobile', 'Referer': 'Bing', 'Language': 'EN'}
        age = context.get('Age')        # Example: 42.0
        agent = context.get('Agent')    # Example: 'mobile'
        id = context.get('ID')          # Example: 236
        referer = context.get('Referer')    # Example: 'Bing'
        language = context.get('Language')  # Example: 'EN'
        return obj, context, age, agent, id, referer, language

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