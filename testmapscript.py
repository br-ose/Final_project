import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import os.path
import csv
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

        # global_db_name = 'testdb2' # database file name

        # def setUpDatabase(db_name): # function that creates/connects us to the SQL database
        #         path = os.path.dirname(os.path.abspath(__file__))
        #         conn = sqlite3.connect(path + '/' + db_name)
        #         cur = conn.cursor()
        #         return cur, conn

        # if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/' + global_db_name): # if the database doesn't exist yet,
        #     global_cur, global_conn = setUpDatabase(global_db_name) # make it! (apparently simply calling the setUpDatabase function creates it?)
        #     global_cur.execute("DROP TABLE IF EXISTS Main_Table") # just to be safe, format the database of any existing Main_Table
        #     global_cur.execute("CREATE TABLE Main_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, point_name TEXT, longitude REAL, latitude REAL)")
        #     for anyentry in worldgdf['iso_a3']:
        #         global_cur.execute("INSERT INTO Main_Table (point_name, longitude, latitude) VALUES (?, ?, ?)", (anyentry, None, None))
        #     global_conn.commit()
        #     print("\nDatabase created!\n") # statement for user to see a new database was created

        # else: # if the databse already exists,
        #     global_cur, global_conn = setUpDatabase(global_db_name) # just connect to it!
        #     print("\nDatabase already created, using existing database!\n") # statement for user to see they accessed the existing database

    def getemissions(self,country):
    # Get average carbon monoxide emissions across a given country for the past period
    ## Get average recent emissions
    # use fixed full date
        url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin={}&end={}".format(country,"2017","2019")
        datavar =  requests.get(url)
        jsonvar = datavar.json()
        # self.emissionsresults = # emissions ???

    def gettemp(self,country):
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country)   
        datavar =  requests.get(url)
        jsonvar = datavar.json()

    def addtemp(self,tempdata,global_cur,global_conn):
        ## adds the temp data to the database in chunks
        #Shared key is coords
        pass

    def addemissions(self,emdata):
        # adds emissions data in chunks
        #Shared key is country
        pass

    def calculateavg(self):
        # gets the average emissions of a country and compares 
        pass

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

    def autocomplete(self):

        while len(self.userinputlist) < 25:
            chosencountry = random.choice(self.worldgdf['iso_a3'])
            if chosencountry not in self.userinputlist:
                self.userinputlist += [chosencountry]
        
        print(len(self.userinputlist))

    def populateData(self):

        # for anyrow in ben's data table(s):
        #     index_num = list(worldgdf['iso_a3']).index(anyrow's country ### this should be anyrow[2]??? ### )
        #     (worldgdf.at[index_num, 'datacolumn1'], worldgdf.at[index_num, 'datacolumn2']) = (datavalue1, datavalue2)

        randomvalslist = [random.random() + 1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        randomvalslist2 = [1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        self.worldgdf['randomvals'], self.worldgdf['randomvals2'] = randomvalslist, randomvalslist2

        #global_conn.close()

    def showMap(self):

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

newInstance = doneWithTheEarth()

newInstance.getUserInput()
newInstance.autocomplete()
newInstance.populateData()
newInstance.showMap()