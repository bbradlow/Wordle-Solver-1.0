import math
from sqlite3 import Row
import numpy as np
import csv

#Made by Ben Bradlow

FileToOpen = "/Users/benjaminbradlow/Desktop/Woldarb/FiveLetterWords.txt"
Freqs = "/Users/benjaminbradlow/Desktop/Woldarb/EnglishLetFreq.txt"
freqlet = []
VowelList = ["a","e","i","o","u"]

EliminatedLetters = list("adiu")
LettersInWord = list("tore")
LettersInRightSpot = list("   er")
LettersNotInRightSpot = [["t",0],["o",1],["",2],["",3,0]] #0 is the first pos

TopBlank = 5
LengthOfWords = 5
RepititionCutOff = 5 #The one thing that is human skill

class Opener:
    def __init__(self):
        self.beginsolve = Solver()

    def OpenFile(self):
        global freqlet
        with open(FileToOpen) as self.f:
            self.lines = self.f.readlines()
        with open(Freqs) as self.w:
            self.freqs = self.w.readlines()
            freqlet = self.freqs
        self.beginsolve.Go(self.lines)


class Solver:
    def __init__(self):
        pass

    def Set(self):
        global RepititionCutOff
        self.SortAll = self.SortByAll(self.lines)
        self.SortCon = self.SortByContained(self.lines)
        self.SortSpo = self.SortBySpot(self.lines)
        self.SortInv = self.SortByInvalid(self.lines)
        self.SortVow = self.SortByVowelInvalid(self.lines)
        if len(EliminatedLetters) == 0:
            self.totaloutput = [self.SortAll]
            self.names = ["Best Word(s)"]
        if len(EliminatedLetters) > 0:
            self.totaloutput = [self.SortCon,self.SortSpo,self.SortInv]
            self.names = ["Contain(ed)","Position(s)","Valid(s)"]
        '''
        self.FirstWord = self.SortInv[0]
        self.NumOfFirstWord = self.FirstWord[0]
        if self.NumOfFirstWord < 0 and RepititionCutOff > 10:
            RepititionCutOff = 5
            self.Set()
        '''


    def Go(self,List):
        self.lines = List

        self.Set()
        #print(RepititionCutOff)

        for num in range(len(self.totaloutput)):
            print("")
            print("By: "+self.names[num])
            print("Length: "+str(len(self.totaloutput[num]))+" (Top "+str(TopBlank)+")")
            if len(self.totaloutput[num]) >= TopBlank:
                for word in range(TopBlank):
                    self.boom = self.totaloutput[num]
                    self.GH = self.boom[word]
                    self.MF = self.GH[1]
                    print(str(round(self.GH[0],5))+" "+str(self.MF[0:LengthOfWords]))
            if len(self.totaloutput[num]) < TopBlank:
                for word in range(len(self.totaloutput[num])):
                    self.boom = self.totaloutput[num]
                    self.GH = self.boom[word]
                    self.MF = self.GH[1]
                    print(str(round(self.GH[0],5))+" "+str(self.MF[0:LengthOfWords]))
        print("")

    def SortByAll(self,List):
        self.WordsList = List
        self.WordsWithReps = []

        #For Repititions
        if len(EliminatedLetters) < RepititionCutOff:
            for row in range(len(self.WordsList)):
                self.CurrentWord = self.WordsList[row]
                self.Repeated = False
                for letter in range(len(self.CurrentWord)):
                    self.WordList = list(self.CurrentWord[0:5])
                    self.repititions = self.WordList.count(self.CurrentWord[letter])
                    if self.repititions > 1:
                        self.Repeated = True
                if self.Repeated == True:
                    self.WordsWithReps.append(self.CurrentWord)
            for row in range(len(self.WordsWithReps)):
                if self.WordsWithReps[row] in self.WordsList:
                    self.WordsList.remove(self.WordsWithReps[row])

        #For Vowel Emphasis
        self.VowelsAmountList = []
        self.EvenBetterWordsList = []
        for row in range(len(self.WordsList)):
            self.CurrentWordVowels = 0
            self.CurrentWord = self.WordsList[row]
            for letter in range(len(self.CurrentWord)):
                if self.CurrentWord[letter] in VowelList:
                    self.CurrentWordVowels += 1
            self.VowelsAmountList.append(self.CurrentWordVowels)

        for row in range(len(self.VowelsAmountList)):
            if self.VowelsAmountList[row] == max(self.VowelsAmountList):
                self.EvenBetterWordsList.append(self.WordsList[row])

        return self.SortByScrabble(self.EvenBetterWordsList)
    
    def SortByScrabble(self,List):
        self.Result = []
        self.ValuesList = []
        self.UseThis = List
        #print(RepititionCutOff)
        for row in range(len(self.UseThis)):
            self.CurrentWordValue = 0
            self.CurrentRow = self.UseThis[row]
            for letter in range(len(self.CurrentRow)):
                if self.CurrentRow[letter] in EliminatedLetters:
                    self.CurrentWordValue -= 1000
                for num in range(len(freqlet)):
                    self.freqletrow = freqlet[num]
                    if self.CurrentRow[letter] == self.freqletrow[0]:
                        self.CurrentWordValue += float(self.freqletrow[2:6])

            self.ValuesList.append([self.CurrentWordValue,self.CurrentRow])
            self.ValuesList.sort(reverse = True)
        return self.ValuesList

    def SortByContained(self,List):
        self.UseMe = List
        self.HaveLetterIn = []
        for row in range(len(self.UseMe)):
            self.CurrentWerd = self.UseMe[row]
            self.Contained = 0
            self.SpacingErrorCorrection = self.CurrentWerd[0:LengthOfWords]
            for letternum in range(len(LettersInWord)):
                if LettersInWord[letternum] in self.SpacingErrorCorrection:
                    self.Contained += 1
            if self.Contained == len(LettersInWord):
                self.HaveLetterIn.append(self.SpacingErrorCorrection)

        return self.SortByScrabble(self.HaveLetterIn)

    def SortBySpot(self,List):
        self.UseIt = self.SortByContained(List)
        self.HaveLetterSpot = []
        for row in range(len(self.UseIt)):
            self.CurrentWerd = self.UseIt[row]
            self.CurrentCol = self.CurrentWerd[1]
            self.Contained = 0
            self.SpacingErrorCorrection = self.CurrentCol[0:LengthOfWords]
            for letternum in range(len(self.SpacingErrorCorrection)):
                if self.SpacingErrorCorrection[letternum] == LettersInRightSpot[letternum]:
                    self.Contained += 1
                if LettersInRightSpot[letternum] == " ":
                    self.Contained += 1
            if self.Contained == len(LettersInRightSpot):
                self.HaveLetterSpot.append(self.SpacingErrorCorrection)

        return self.SortByScrabble(self.HaveLetterSpot)

    def SortByInvalid(self,List):
        self.UsePower = self.SortBySpot(List)
        self.NoInvalidPos = []
        for word in range(len(self.UsePower)):
            self.InvalidPos = False
            self.Test = self.UsePower[word]
            self.CurrWord = self.Test[1]
            for letter in range(len(self.CurrWord)):
                self.CurrLetter = self.CurrWord[letter]
                for elimletter in range(len(LettersNotInRightSpot)):
                    self.Spot = [self.CurrLetter,letter]
                    self.ElimLetter = LettersNotInRightSpot[elimletter]
                    for lengthelim in range(1,len(self.ElimLetter)):
                        self.CurrSpot = [self.ElimLetter[0],self.ElimLetter[lengthelim]]
                        if self.Spot == self.CurrSpot:
                            self.InvalidPos = True
            if self.InvalidPos == False:
                self.NoInvalidPos.append([self.Test[0],self.CurrWord])

        return self.NoInvalidPos

    def SortByVowelInvalid(self,List):
        pass

class Tester():
    def Test(self):
        pass
        

if __name__ == "__main__":
    #summarizer = Tester()
    #summarizer.Test()
    summarizer = Opener()
    summarizer.OpenFile()