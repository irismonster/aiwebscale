from basics import rest_interaction
# Voor tessa: from practical.basics import rest_interaction

class Main:

    teamID = 'Error_Teamname_not_found'
    teamPW = '845ea0b18db9a82bc43c811d740d3177'


    def __init__(self):
        print("Hello world")
        runID = 10
        numberOfIs = 10

        ri = rest_interaction
        r = ri.RestInteraction(self.teamID, self.teamPW)
        r.loopOverPeople(runID, numberOfIs)

m = Main()