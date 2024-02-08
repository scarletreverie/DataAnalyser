import csv
import time

fileName = input("Enter the name of the data file: ")

with open(fileName, "r") as soccerDataFile:

    dataReader = csv.reader(soccerDataFile)
        
    def lastXMatchResults(team, matchDate, numberOfResults):

        lastResults = []
        
        for line in enumerate(dataReader):
            homeScore = 0
            awayScore = 0
            matchResult = ""
            teamResult = ""
            try:
                homeScore = int(line[8].split("-")[0])
                awayScore = int(line[8].split("-")[1])

                if (homeScore > awayScore):
                    matchResult = "home"
                if (awayScore > homeScore):
                    matchResult = "away"
                if (homeScore == awayScore):
                    matchResult = "draw"
                    
            except ValueError:
                if (line[8] != "Score" and line[8] != "Fouls Committed"):
                    print(line[8])
                    print("An Error occurred extracting the score from line: " + str(i))
            
            except IndexError:
                pass
            if (line[0] == matchDate):
                if(len(lastResults) < numberOfResults):
                    print("Only " + str(len(lastResults)) + " of requested " + str(numberOfResults) + " last results available.")
                return lastResults
            try:
                if (line[2] == team):
                    if(matchResult == "home"):
                        teamResult = "win"
                    if(matchResult == "draw"):
                        teamResult = "draw"
                    if(matchResult == "away"):
                        teamResult = "loss"
                if (line[3] == team):
                    if(matchResult == "home"):
                        teamResult = "loss"
                    if(matchResult == "draw"):
                        teamResult = "draw"
                    if(matchResult == "away"):
                        teamResult = "win"
            except IndexError:
                pass

            if(teamResult != ""):
                if(len(lastResults) == numberOfResults):
                    lastResults.pop(0)
                    lastResults.append(teamResult)
                if(len(lastResults) < numberOfResults):
                    lastResults.append(teamResult)

        def featuresPastXGames(team, matchDate, feature, numberOfResults):

            featureArray = []
            statSum = 0
            numberOfStats = 0
            totalMinutesPlayed = 0
            statIndices = {"Minutes Played": 1, "Goals": 2, "Assists": 3, "Shots on Target": 5, "Crosses": 11, "Tackles Won": 12, "Interceptions": 13, "Position": 14}
            readingFromMatch = True
            
            for line in enumerate(dataReader):
                if (line[0] == "Date"):
                    readingFromMatch = False
                    
                if ((line[2] == team or line[3] == team) and line[0] != matchDate):
                    readingFromMatch = True
                    
                if (readingFromMatch):
                    if((feature == "Shots on Target") and (line[statIndices["Position"]][0] == "a")):
                        statSum += int(line[statIndices[feature]])
                        numberOfStats += 1
                        totalMinutesPlayed += int(line[statIndices["Minutes Played"]])
                if ((line[2] == team or line[3] == team) and line[0] == matchDate):
                    return featureArray

            avgPerPlayerPerMinute = (statSum/numberOfStats)/totalMinutesPlayed
                
        #Work out how many standard deviations the team is above or below for features on average over their past X games
        #sqrt((sample-mean)^2/(n-1))
        #Work out an array of features conceded by opponent in their last X games
        def getAverageStandardDeviationLastXResults(team, matchDate, feature, numberOfResults):

            lastResults = []
            statSum = 0
            numberOfStats = 0
            totalMinutesPlayed = 0
            statIndices = {"Minutes Played": 1, "Goals": 2, "Assists": 3, "Shots on Target": 5, "Crosses": 11, "Tackles Won": 12, "Interceptions": 13, "Position": 14}
            readingFromMatch = True
            for line in enumerate(dataReader):
                if (line[0] == "Date"):
                    readingFromMatch = False
                if (line[2] == team or line[3] == team):
                    readingFromMatch = True
                    if(readingFromMatch):
                        try:
                            if(feature == "Shots on Target"):
                                #Player positions are stored in the dataset according to a code where the first letter indicates attack, centre, or defence
                                if(line[statIndices["Position"]][0] == "a"):
                                    statSum += int(line[statIndices[feature]])
                                    numberOfStats += 1
                                    totalMinutesPlayed += int(line[statIndices["Minutes Played"]])                              

            #The feature's average per player per minute
            avgPerPlayerPerMinute = (statSum/numberOfStats)/totalMinutesPlayed
            
            featureStandardDeviation
                    
                    
                    
                
                
    getAverageStandardDeviationLastXResults("Central Coast Mariners", "03/02/2024", "Shots on Target", 5))
