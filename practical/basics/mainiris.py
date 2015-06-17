from practical.basics import rest_interaction
# Voor tessa: from practical.basics import rest_interaction

class Main:

    teamID = 'Error_Teamname_not_found'
    teamPW = '845ea0b18db9a82bc43c811d740d3177'


    def __init__(self):
        print("Hello world")
        runs = 1
        numberOfIs = 10

        ri = rest_interaction
        r = ri.RestInteraction(self.teamID, self.teamPW)
        meanMean = 0
        meanVariance = 0
        for i in range(runs):
            print("run: " + str(i))
            mean, variance = r.loopOverPeople(i, numberOfIs)
            meanMean = meanMean + (mean - meanMean) / (i+1)
            meanVariance = meanVariance + (variance - meanVariance) / (i+1)
        print("Mean mean : " + str(meanMean))
        print("Mean var : " + str(meanVariance))

m = Main()