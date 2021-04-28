import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import os.path
import random
import sqlite3
import requests
import json

class doneWithTheEarth:

    def __init__(self):

        self.userinputlist = []
        self.yeartuple = (1901, 2012)

        datapath = gpd.datasets.get_path('naturalearth_lowres') # sets map we're using to a default map of the whole world
        self.worldgdf = gpd.read_file(datapath)
        (self.worldgdf.at[21, 'iso_a3'], self.worldgdf.at[43, 'iso_a3'], self.worldgdf.at[174, 'iso_a3']) = ('NOR', 'FRA', 'XKX') # adds Norway, France, Kosovo

        # i'm gonna redo the database stuff in a minute

        global_db_name = 'testdb2' # database file name

        def setUpDatabase(db_name): # function that creates/connects us to the SQL database
            path = os.path.dirname(os.path.abspath(__file__))
            conn = sqlite3.connect(path + '/' + db_name)
            cur = conn.cursor()
            return cur, conn

        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/' + global_db_name): # if the database doesn't exist yet,
            self.global_cur, self.global_conn = setUpDatabase(global_db_name) # make it! (apparently simply calling the setUpDatabase function creates it?)
            self.global_cur.execute("DROP TABLE IF EXISTS Emissions_Data") # just to be safe, format the database of any existing Main_Table    
            self.global_cur.execute("CREATE TABLE Emissions_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_a3 TEXT, emissions REAL)")
            self.global_cur.execute("DROP TABLE IF EXISTS Temperature_Data") # just to be safe, format the database of any existing Main_Table
            self.global_cur.execute("CREATE TABLE Temperature_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_a3 TEXT, tempchange REAL, startyear INTEGER, endyear INTEGER)")
            self.global_conn.commit()
        #     for anyentry in worldgdf['iso_a3']:
        #         global_cur.execute("INSERT INTO Main_Table (point_name, longitude, latitude) VALUES (?, ?, ?)", (anyentry, None, None))
        #     global_conn.commit()
            print("\nDatabase created!\n") # statement for user to see a new database was created

        else: # if the databse already exists,
            self.global_cur, self.global_conn = setUpDatabase(global_db_name) # just connect to it!
            print("\nDatabase already created, using existing database!\n") # statement for user to see they accessed the existing database

    def __str__(self):

        return "This is an object of our class we created, man! You can't just print it!\n\nTake a look at our documentation to learn what to do!"

    def getemissions(self,country):

    ## Get average recent emissions
    # use fixed full date
    # returns average
        url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin=2018-12-31&end=2021-4-25".format(country)
        results =  requests.get(url,timeout=5)
        results = results.json()
        totalresult = 0
        for result in results:
            totalresult += result["average"] 
        totalresult = totalresult/len(results)
        return totalresult

    def gettemp(self,country,year1,year2):
        ## Both years should be positive integers and year 2 should be a greater number than year 1
        ### year1 is lower bound year2 is higher one
        ### coordinates is coordinates
        ### Returns the difference
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country.strip())
        print(url) 
        results =  requests.get(url,timeout=5)
        results = results.json()
        ## This is just difference in two values
        for result in results:
            if result["year"] == int(year1):
                lowerdata = result["data"]
            if result["year"] == int(year2):
                higherdata = result["data"]
        try:
            lowerdata
        except NameError:
            print("Earlier year not in the database!")
            return 0 
        try:
            higherdata
        except NameError:
            print("Later year not in the database!")
            return 0
        return higherdata - lowerdata

    def getUserInput(self):

        loopbool = True
        loopbool2 = True

        while loopbool:
            userinput = input("Input an ISO3 country code to compare it to other countries on a map, or type 'exit': ").upper()
            if userinput == 'EXIT':
                loopbool = False
            elif userinput.isalpha() and len(userinput) == 3 and userinput in list(self.worldgdf['iso_a3']) and len(self.userinputlist) < 25:
                self.userinputlist += [userinput]
            elif len(self.userinputlist) >= 25:
                print("Maximum (25) entries made this session, please type 'exit'.")
                continue
            else:
                print("Invalid input, try again.")
                continue

        while loopbool2:
            userinput2 = input("Give me a year, a space, and then another year (range 1901-2012): ")
            if (userinput2[:4].isdigit() 
            and len(userinput2[:4]) == 4 
            and int(userinput2[:4]) >= 1901 
            and int(userinput2[:4]) <= 2012 
            and userinput2[4] == ' ' 
            and userinput2[5:].isdigit()
            and len(userinput2[5:]) == 4
            and int(userinput2[5:]) >= 1901
            and int(userinput2[5:]) <= 2012):
                self.yeartuple = (int(userinput2[:4]), int(userinput2[5:]))
                loopbool2 = False
            else:
                print("Invalid input, try again.")
                continue

    def populateEmissionsData(self):

        self.global_cur.execute("SELECT iso_a3 FROM Emissions_Data")
        datalist = [anyentry[0] for anyentry in list(self.global_cur.fetchall())]
        accum = 0
        for anycountry in self.worldgdf['iso_a3']:
            if anycountry not in datalist and accum < 10:
                self.global_cur.execute("INSERT INTO Emissions_Data (iso_a3, emissions) VALUES (?, ?)", (anycountry, self.getemissions(anycountry)))
                print("Added {}'s emissions to the database!".format(anycountry))
                accum += 1
            elif accum >= 10:
                break
        self.global_conn.commit()

    def populateTempData(self):

        self.global_cur.execute("SELECT iso_a3, startyear, endyear FROM Temperature_Data")
        fulllist = list(self.global_cur.fetchall())
        namelist = [anyentry[0] for anyentry in fulllist]
        accum = 0
        for anycountry in self.worldgdf['iso_a3']:
            # for anycountry in the world,
            # if anycountry is already stored in the database but the year is wrong,
            # delete the current entry and make a new one
            # if anycountry is already stored in the database but the year is right,
            # leave it alone
            # if anycountry is not already stored in the database,
            # add it with the right year
            if accum >= 10:
                break
            if anycountry in namelist: # and the year is different than the one on file;
                fulllistentry = fulllist[namelist.index(anycountry)]
                if (fulllistentry[1], fulllistentry[2]) != self.yeartuple and accum < 10:
                    self.global_cur.execute("DELETE FROM Temperature_Data WHERE iso_a3 = ?", (anycountry,)) # delete and replace 
                    self.global_cur.execute("INSERT INTO Temperature_Data (iso_a3, tempchange, startyear, endyear) VALUES (?, ?, ?, ?)", (anycountry, self.gettemp(anycountry, self.yeartuple[0], self.yeartuple[1]), self.yeartuple[0], self.yeartuple[1]))
                    accum += 1
                elif (fulllistentry[1], fulllistentry[2]) == self.yeartuple:
                    pass
            elif anycountry not in namelist and accum < 10:
                self.global_cur.execute("INSERT INTO Temperature_Data (iso_a3, tempchange, startyear, endyear) VALUES (?, ?, ?, ?)", (anycountry, self.gettemp(anycountry, self.yeartuple[0], self.yeartuple[1]), self.yeartuple[0], self.yeartuple[1]))
                accum += 1

        self.global_conn.commit()
    
    def calculatedata(self):
        cur.execute("SELECT iso_a3,emissions FROM Emissions_Data where emissions = (SELECT MAX(emissions) FROM Emissions_Data)")
        highest = cur.fetchone()
        cur.execute("SELECT iso_a3,emissions FROM Emissions_Data where emissions = (SELECT MIN(emissions) FROM Emissions_Data)")
        lowest = cur.fetchone()
        print(highest)
        print(lowest)
        cur.execute("SELECT Emissions_Data.iso_a3,Emissions_Data.emissions,Temperature_Data.tempchange FROM Emissions_Data JOIN Temperature_Data ON Emissions_Data.iso_a3 = Temperature_Data.iso_a3 WHERE Emissions_Data.emissions = ?;",(highest[1],))
        highestval = cur.fetchone()
        cur.execute("SELECT Emissions_Data.iso_a3,Emissions_Data.emissions,Temperature_Data.tempchange Temperature_Data. FROM Emissions_Data JOIN Temperature_Data ON Emissions_Data.iso_a3 = Temperature_Data.iso_a3 WHERE Emissions_Data.emissions = ?;",(lowest[1],))
        lowestval = cur.fetchone()
        f = open("highestandlowest.txt","w")
        f.write("The ISO3 code of the country with the highest recent carbon monoxide emissions was {}.\nIt emitted {} mol/m^2 of carbon monoxide on average over the past 3 years, and experienced a {} degree celcius change in average temperature over the past {} years.\n".format(highestval[0],highestval[1],highestval[2],self.yeartuple[1]-self.yeartuple[0]))
        f.write("The ISO3 code of the country with the lowest recent carbon monoxide emissions was {}.\nIt emitted {} mol/m^2 of carbon monoxide on average over the past 3 years, and experienced a {} degree celcius change in average temperature over the past {} years.\n".format(lowestval[0],lowestval[1],lowestval[2],self.yeartuple[1]-self.yeartuple[0]))
        f.close()

    def autocomplete(self):

        while len(self.userinputlist) < 25:
            chosencountry = random.choice(self.worldgdf['iso_a3'])
            if chosencountry not in self.userinputlist:
                self.userinputlist += [chosencountry]
        
        # print(len(self.userinputlist))

    def summonData(self):

        # for anyrow in ben's data table(s):
        #     index_num = list(worldgdf['iso_a3']).index(anyrow's country ### this should be anyrow[2]??? ### )
        #     (worldgdf.at[index_num, 'datacolumn1'], worldgdf.at[index_num, 'datacolumn2']) = (datavalue1, datavalue2)

        #randomvalslist = [random.random() + 1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        #randomvalslist2 = [1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        #self.worldgdf['randomvals'], self.worldgdf['randomvals2'] = randomvalslist, randomvalslist2

        #self.global_cur.execute("SELECT iso_a3, emissions FROM Emissions_Data")
        #emissionsdatalist = list(self.global_cur.fetchall())

        #countrycodes = 
        #self.userinputlist = [(anyentry, list(self.worldgdf['iso_a3']).index(anyentry)) for anyentry in self.userinputlist]
        
        self.userinputlist = sorted(self.userinputlist, key = lambda a: list(self.worldgdf['iso_a3']).index(a))
        
        emissiondatalist = []
        for anycountry in list(self.worldgdf['iso_a3']):
            if anycountry in self.userinputlist:
                self.global_cur.execute("SELECT iso_a3, emissions FROM Emissions_Data")
                emissiondatapoints = self.global_cur.fetchall()
                emissiondatalist += [anyentry[1] for anyentry in emissiondatapoints if anyentry[0] == anycountry]
            else:
                emissiondatalist += [None]

        self.worldgdf['emissions'] = emissiondatalist

        tempdatalist = []
        for anycountry in list(self.worldgdf['iso_a3']):
            if anycountry in self.userinputlist:
                self.global_cur.execute("SELECT iso_a3, tempchange FROM Temperature_Data")
                tempdatapoints = self.global_cur.fetchall()
                tempdatalist += [anyentry[1] for anyentry in tempdatapoints if anyentry[0] == anycountry]
            else:
                tempdatalist += [None]

        self.worldgdf['tempchange'] = tempdatalist

        # pull up emissions data
        # pull up contry data from self.worldgdf['iso_a3'] or maybe self.worldgdf['id']???
        # templist = []
        # for anycountry in self.userinputdata:
        #     templist 

    def showMap(self):

        self.global_conn.close()

        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['emissions'], cmap = 'viridis', legend = True)
        plt.title('Some cool climate change data (mol/m^3)') # gives our map a title
        plt.xlabel('Longitude') # name the x and y axes,
        plt.ylabel('Latitude')
        plt.figure(1)
        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['tempchange'], cmap = 'viridis', legend = True)
        plt.title('Temperature change from {} to {}'.format(str(self.yeartuple[0]), str(self.yeartuple[1])))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

newInstance = doneWithTheEarth()

#newInstance.getUserInput()
#newInstance.autocomplete()
#newInstance.populateData()
newInstance.populateEmissionsData()
newInstance.populateTempData()
#newInstance.summonData()
#newInstance.showMap()