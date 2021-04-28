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
        results =  requests.get(url)
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
        results =  requests.get(url)
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
        datalist = list(self.global_cur.fetchall())
        for anycountry in self.worldgdf['iso_a3']:
            if anycountry not in datalist:
                self.global_cur.execute("INSERT INTO Emissions_Data (iso_a3, emissions) VALUES (?, ?)", (anycountry, self.getemissions(anycountry)))
        self.global_cur.commit()

    def populateTempData(self):

        self.global_cur.execute("SELECT iso_a3 FROM Temperature_Data")
        datalist = list(self.global_cur.fetchall())
        for anycountry in self.worldgdf['iso_a3']:
            if anycountry in datalist:
                self.global_cur.execute("DELETE FROM Temperature_Data WHERE iso_a3 = ?", (anycountry,))
            self.global_cur.execute("INSERT INTO Temperature_Data (iso_a3, tempchange, startyear, endyear) VALUES (?, ?, ?, ?)", (anycountry, self.gettemp(anycountry), self.yeartuple[0], self.yeartuple[1]))
        self.global_cur.commit()
    
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

    def showMap(self):

        self.global_conn.close()

        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['randomvals'], cmap = 'viridis', legend = True)
        plt.title('Some cool climate change data (mol/m^3)') # gives our map a title
        plt.xlabel('Longitude') # name the x and y axes,
        plt.ylabel('Latitude')
        plt.figure(1)
        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['randomvals2'], cmap = 'viridis', legend = True)
        plt.title('Temperature change from {} to {}'.format(str(self.yeartuple[0]), str(self.yeartuple[1])))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

#newInstance = doneWithTheEarth()

#newInstance.getUserInput()
#newInstance.autocomplete()
#newInstance.populateData()
#newInstance.showMap()