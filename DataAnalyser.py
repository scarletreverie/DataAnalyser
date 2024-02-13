import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import time

POPULATION_SAMPLE_SIZE = 5

attackingFeatures = ["Goals", "Assists", "Shots", "Shots on Target", "Crosses", "Tackles Won", "Interceptions"]
statIndices = {"Minutes Played": 1, "Goals": 2, "Assists": 3, "Shots": 4, "Shots on Target": 5, "Crosses": 11, "Tackles Won": 12, "Interceptions": 13, "Position": 14}
teams = ["Adelaide United", "Brisbane Roar", "Central Coast Mariners", "Macarthur FC", "Newcastle Jets", "Melbourne City", "Melbourne Victory", "Perth Glory", "Sydney FC", "Wellington Phoenix", "Western Sydney Wanderers", "Western United"]

fileName = input("Enter the name of the data file: ")

def standardDeviation(sampleArray):
    
    sampleMean = 0
    sampleSum = 0
    for i in range(len(sampleArray)):
        sampleSum += float(sampleArray[i])
    sampleMean = sampleSum/len(sampleArray)

    variance = 0
    distanceSum = 0
    for i in range(len(sampleArray)):
        distanceSum += (sampleArray[i] - sampleMean)**2

    stdDeviation = math.sqrt(distanceSum/(len(sampleArray)-1))
    return stdDeviation
        
def median(sampleArray):
    sampleArray.sort()
    arrayLength = len(sampleArray)
    if (arrayLength == 0):
        raise Exception("Error: Cannot calculate median of empty array")
    if (arrayLength == 1):
        return sampleArray[0]
    if (arrayLength == 2):
        return (sampleArray[0] + sampleArray[1])/2
    if (len(sampleArray) % 2 == 1):
        return (sampleArray[int((arrayLength-1)/2)])
    else:
        return ((sampleArray[int(arrayLength/2)] + sampleArray[int(arrayLength/2-1)])/2)

def outlierIndices(array1):
    indices = []
    for i in range(len(array1)):
        if(abs(array1[i] - np.median(array1))/np.std(array1) > 2):
            indices.append(i)
    return indices

#Point-biserial correlation
def calculatePBC(array1, array2, showGraph = False, xTitle = "Default", yTitle = "Default"):
    if (len(array1) != len(array2)):
        raise Exception("Error: Cannot calculate PBC for sample arrays of different lengths")

    winSamples = []
    nonWinSamples = []

    deletionIndices = outlierIndices(array1)
    array1 = np.delete(array1, deletionIndices)
    array2 = np.delete(array2, deletionIndices)
  
    for i in range(len(array1)):
        if (array2[i] == 0):
            nonWinSamples.append(array1[i])
        else:
            winSamples.append(array1[i])

    winSamples = np.array(winSamples)
    nonWinSamples = np.array(nonWinSamples)
    deletionIndicesWinSamples = outlierIndices(winSamples)
    deletionIndicesNonWinSamples = outlierIndices(nonWinSamples)

    winSamples = np.delete(winSamples, deletionIndicesWinSamples)
    nonWinSamples = np.delete(nonWinSamples, deletionIndicesNonWinSamples)

    winSamplesMean = np.mean(winSamples)
    nonWinSamplesMean = np.mean(nonWinSamples)
    
    sampleStdDeviation = np.std(np.concatenate((winSamples, nonWinSamples)))
    
    PBC = ((winSamplesMean - nonWinSamplesMean)/sampleStdDeviation)*(math.sqrt(((len(winSamples)*len(nonWinSamples))/((len(array1)+len(array2))**2))))

    print(PBC)

    if(showGraph):
        plt.xlabel(xTitle)
        plt.ylabel(yTitle)
        plt.boxplot([nonWinSamples, winSamples], labels=["Non win","Win"])
        #plt.scatter(array2, array1, s=10, color ='b')
        #plt.xticks([0,1])
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
    
    def lastXMatchResults(team, matchDate, numberOfResults = POPULATION_SAMPLE_SIZE):

        lastResults = []
        
        for line in data:
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

    #Returns an array of the average results for a conceded feature in each of the last X games of a team
    def featureAvgsPastXGames(team, matchDate, feature):
        
        featureArray = []
        statSum = 0
        totalMinutesPlayed = 0
        readingFromMatch = False
        readingTeamStats = False
        
        for line in data:
            if (line[0] == "Date" and readingFromMatch):
                avgPerPlayerPerMinute = (90*statSum)/(totalMinutesPlayed**2)
                if(len(featureArray) == POPULATION_SAMPLE_SIZE):
                    featureArray.pop(0)
                featureArray.append(avgPerPlayerPerMinute)
                statSum = 0
                totalMinutesPlayed = 0
                readingFromMatch = False
                
            try:
                if (line[2] == team or line[3] == team):
                    readingFromMatch = True
            except IndexError:
                pass

            if (readingFromMatch):
                try:
                    if ((line[2] == team or line[3] == team) and line[0] == matchDate):
                        return featureArray
                    if(readingTeamStats):
                        if((feature in attackingFeatures) and (line[statIndices["Position"]][0] == "a")):
                            statSum += int(line[statIndices[feature]])
                            totalMinutesPlayed += int(line[statIndices["Minutes Played"]])
                except IndexError:
                    pass
                if(readingTeamStats and len(line) < 2):
                    readingTeamStats = False
                if(line[0] in teams and line[0] != team):
                    readingTeamStats = True
                
    #Returns the average amount of standard deviations above or below the average a team has
    #managed for a feature in its past X games
    def getMedianStandardDeviation(team, matchDate, feature):

        readingFromMatch = False
        matchCounter = 0
        specificMatchDate = ""
        opposingTeam = ""
        statSum = 0
        totalMinutesPlayed = 0
        featureArray = []
        opposingTeam = ""
        readingTeamStats = False
        
        for line in data:
            if (line[0] == "Date" and readingFromMatch and matchCounter > POPULATION_SAMPLE_SIZE):
                stdDeviation = standardDeviation(featureAvgsPastXGames(opposingTeam, specificMatchDate, feature))
                avgPerPlayerPerMinute = (90*statSum)/(totalMinutesPlayed**2)

                sampleMean = np.median(np.array(featureAvgsPastXGames(opposingTeam, specificMatchDate, feature)))
                
                try:
                    teamStdDeviation = (avgPerPlayerPerMinute-sampleMean)/stdDeviation
                except ZeroDivisionError:
                    teamStdDeviation = (avgPerPlayerPerMinute-sampleMean)/0.001

                if(len(featureArray) == POPULATION_SAMPLE_SIZE):
                    featureArray.pop(0)
                featureArray.append(teamStdDeviation)
                statSum = 0
                totalMinutesPlayed = 0
                readingFromMatch = False
            try:
                if (line[2] == team or line[3] == team):
                    matchCounter += 1
                    readingFromMatch = True
                    specificMatchDate = line[0]
                    if (line[2] == team):
                        opposingTeam = line[3]
                    if (line[3] == team):
                        opposingTeam = line[2]
                    if (line[0] == matchDate):
                        return median(featureArray)
            except IndexError:
                pass
            if(readingFromMatch):
                try:
                    if(readingTeamStats):
                        if((feature in attackingFeatures) and (line[statIndices["Position"]][0] == "a")):
                            statSum += int(line[statIndices[feature]])
                            totalMinutesPlayed += int(line[statIndices["Minutes Played"]])
                except IndexError:
                    pass
                if(readingTeamStats and len(line) < 2):
                    readingTeamStats = False
                if(line[0] == team):
                    readingTeamStats = True
        raise Exception("Error obtaining median standard deviation for past games.")
    
    #Analyses correlation of feature with respect to wins
    def correlateFeature(feature):
        featureArray = []
        matchResults = []
        for team in teams:
            lastMatchDate = getLastMatchDate(team)
            
            for i in lastXMatchResults(team, lastMatchDate):
                if (i == "win"):
                    matchResults.append(1)
                else:
                    matchResults.append(0)
                    
            
            for date in lastXMatchDates(team, lastMatchDate):
                featureArray.append(getMedianStandardDeviation(team, date, feature))

        matchResults = np.array(matchResults)
        featureArray = np.array(featureArray)
        
        calculatePBC(featureArray, matchResults, True, "Match Result", "Median standard deviations of " + feature + " in past " + str(POPULATION_SAMPLE_SIZE) + " games.")

    correlateFeature("Goals")
