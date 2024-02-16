import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import time

POPULATION_SAMPLE_SIZE = 20
PREVIOUS_GAMES_IN_SAMPLE = 10

attackingFeatures = ["Goals", "Assists", "Shots", "Shots on Target", "Crosses", "Tackles Won", "Interceptions"]
statIndices = {"Minutes Played": 1, "Goals": 2, "Assists": 3, "Shots": 4, "Shots on Target": 5, "Crosses": 11, "Tackles Won": 12, "Interceptions": 13, "Position": 14}
teams = ["Adelaide United", "Brisbane Roar", "Central Coast Mariners", "Macarthur FC", "Newcastle Jets", "Melbourne City", "Melbourne Victory", "Perth Glory", "Sydney FC", "Wellington Phoenix", "Western Sydney Wanderers", "Western United"]

fileName = input("Enter the name of the data file: ")
 
def outlierIndices(array):
    indices = []
  
    for i in range(len(array)):
        if(abs(array[i] - np.mean(array))/np.std(array) > 2):
            indices.append(i)
    return indices

#Point-biserial correlation
def calculatePBC(dataArray, showGraph = False, xTitle = "Default", yTitle = "Default"):

    winSamples = []
    nonWinSamples = []

    for i in range(len(dataArray)):
        if (dataArray[i][1] == 0):
            nonWinSamples.append(dataArray[i][0])
        elif (dataArray[i][1] == 1):
            winSamples.append(dataArray[i][0])

    winSamples = np.array(winSamples)
    nonWinSamples = np.array(nonWinSamples)

    winSamplesMean = np.mean(winSamples)
    nonWinSamplesMean = np.mean(nonWinSamples)
    sampleStdDeviation = np.std(np.concatenate((winSamples, nonWinSamples)))
    PBC = ((winSamplesMean - nonWinSamplesMean)/sampleStdDeviation)*(math.sqrt(len(winSamples)*len(nonWinSamples)/(len(dataArray)**2)))

    print(PBC)

    if(showGraph):
        plt.xlabel(xTitle)
        plt.ylabel(yTitle)
        plt.boxplot([nonWinSamples, winSamples], labels=["Non win","Win"])
        plt.show()
    
with open(fileName, "r") as soccerDataFile:

    lines = soccerDataFile.read().splitlines()

    data = list(csv.reader(lines))

    def getLastMatchDate(team):
        date = ""
        for line in data:
            try:
                if (line[2] == team or line[3] == team):
                    date = line[0]
            except:
                pass
        return date
    
    def lastXMatchDates(team, matchDate, numberOfResults = POPULATION_SAMPLE_SIZE):
        lastMatchDates = []
        for line in data:
            if (line[0] == matchDate):
                return lastMatchDates
            try:
                if ((line[2] == team or line[3] == team) and line[0] != matchDate):
                    if(len(lastMatchDates) == numberOfResults):
                        lastMatchDates.pop(0)
                    lastMatchDates.append(line[0])
            except:
                pass

        raise Exception("Error obtaining last match dates.")

    def matchResult(team, matchDate):
        for line in data:
            homeScore = 0
            awayScore = 0
            matchResult = ""
            teamResult = 0
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
                    print("An Error occurred extracting the score from line: " + str(i))
            
            except IndexError:
                pass
            try:
                if (line[2] == team):
                    if(matchResult == "home"):
                        teamResult = 1
                    if(matchResult == "draw"):
                        teamResult = 0
                    if(matchResult == "away"):
                        teamResult = 0
                if (line[3] == team):
                    if(matchResult == "home"):
                        teamResult = 0
                    if(matchResult == "draw"):
                        teamResult = 0
                    if(matchResult == "away"):
                        teamResult = 1
            except IndexError:
                pass
            if (line[0] == matchDate):
                print(team)
                print(matchDate)
                print(teamResult)
                return teamResult
     
    #Returns the average amount of standard deviations above or below the average a team has
    #managed for a feature in its past X games
    #def getMedianStandardDeviation(team, matchDate, feature):
        #Take a team
        #Work out their opponent in their last X Games
        #For each Opponent, find out how much of a feature they conceded in their last Y Games
        

    #Analyses correlation of feature with respect to wins
    def correlateFeature(feature):
        for team in teams:
            for date in lastXMatchDates(team)
                matchResult(team, date)

    correlateFeature("Goals")
