__author__ = 'irismonster'
import numpy as np
import matplotlib.pyplot as plt

sigma = 0.1
mu = 0.3
s = np.random.normal(mu, sigma, 100)

armA = np.random.normal(0.3, 0.1, 1000000)
armB = np.random.normal(0.5, 0.4, 1000000)
armC = np.random.normal(0.7, 0.1, 1000000)

def greedy():
    rewardA = 0
    rewardB = 0
    rewardC = 0
    totalRegret = 0
    for i in range(1000):
        play = 0
        reward = 0
        regret = 0
        if(rewardA == rewardB == rewardC):
            play = np.random.randint(1,4)

        if((rewardA > rewardB and rewardA > rewardC) or play == 1):
            reward = armA[i]

            if(reward < 0.5):
                regret = 1
                rewardA = rewardA + 0
            else:
                regret = 0
                rewardA = rewardA + 1
        else:
            if((rewardB > rewardA and rewardB > rewardC) or play == 2):
                reward = armB[i]
                if(reward < 0.5):
                    regret = 1
                    rewardB = rewardB + 0
                else:
                    regret = 0
                    rewardB = rewardB + 1
            else:
                if((rewardC > rewardA and rewardC > rewardB) or play == 3):
                    reward = armC[i]
                    if(reward < 0.5):
                        regret = 1
                        rewardC = rewardC + 0
                    else:
                        regret = 0
                        rewardC = rewardC + 1

        totalRegret = totalRegret + regret

    print(rewardA)
    print(rewardB)
    print(rewardC)
    print(totalRegret)

def efirst():
    rewardA = 0
    rewardB = 0
    rewardC = 0
    e = 0.3333
    N = 1000
    totalRegret = 0
    for i in range(1000000):
        play = 0
        reward = 0
        regret = 0
        if(i < N):
            play = np.random.randint(1,4)

        if((rewardA > rewardB and rewardA > rewardC and i >= N) or play == 1):
            reward = armA[i]

            if(reward < 0.5):
                regret = 1
                rewardA = rewardA + 0
            else:
                regret = 0
                rewardA = rewardA + 1
        else:
            if((rewardB > rewardA and rewardB > rewardC and i >= N) or play == 2):
                reward = armB[i]
                if(reward < 0.5):
                    regret = 1
                    rewardB = rewardB + 0
                else:
                    regret = 0
                    rewardB = rewardB + 1
            else:
                if((rewardC > rewardA and rewardC > rewardB and i >= N) or play == 3):
                    reward = armC[i]
                    if(reward < 0.5):
                        regret = 1
                        rewardC = rewardC + 0
                    else:
                        regret = 0
                        rewardC = rewardC + 1

        totalRegret = totalRegret + regret

    print(rewardA)
    print(rewardB)
    print(rewardC)
    print(totalRegret)

def ucb():
    rewardA = 0
    rewardB = 0
    rewardC = 0
    totalRegret = 0
    for i in range(1000):
        play = 0
        reward = 0
        regret = 0
        if(rewardA == rewardB == rewardC):
            play = np.random.randint(1,4)

        if((rewardA > rewardB and rewardA > rewardC) or play == 1):
            reward = armA[i]

            if(reward < 0.5):
                regret = 1
                rewardA = rewardA + 0
            else:
                regret = 0
                rewardA = rewardA + 1
        else:
            if((rewardB > rewardA and rewardB > rewardC) or play == 2):
                reward = armB[i]
                if(reward < 0.5):
                    regret = 1
                    rewardB = rewardB + 0
                else:
                    regret = 0
                    rewardB = rewardB + 1
            else:
                if((rewardC > rewardA and rewardC > rewardB) or play == 3):
                    reward = armC[i]
                    if(reward < 0.5):
                        regret = 1
                        rewardC = rewardC + 0
                    else:
                        regret = 0
                        rewardC = rewardC + 1

        totalRegret = totalRegret + regret

    print(rewardA)
    print(rewardB)
    print(rewardC)
    print(totalRegret)

efirst()

#count, bins, ignored = plt.hist(s, 30, normed=True)
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
#plt.show()