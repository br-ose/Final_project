import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import os.path
import csv
import random
import sqlite3

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

    def getUserInput(self):

        loopbool = True
        loopbool2 = True
        accum = 0

        while loopbool:
            userinput = input("Input an ISO3 country code to compare it to other countries on a map, or type 'exit': ")
            if userinput == 'exit':
                loopbool = False
            elif userinput.isalpha() and len(userinput) == 3 and userinput in list(self.worldgdf['iso_a3']) and accum < 25:
                self.userinputlist += [userinput]
                accum += 1
            elif accum >= 25:
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
                yeartuple = (int(userinput2[:4]), int(userinput2[5:]))
                loopbool2 = False
            else:
                print("Invalid input, try again.")
                continue

        # for anyrow in ben's data table(s):
        #     index_num = list(worldgdf['iso_a3']).index(anyrow's country)
        #     worldgdf.at[index_num, 'datacolumn'] = datavalue

    def populateRandomData(self):

        randomvalslist = [random.random() + 1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        randomvalslist2 = [1 if anyentry in self.userinputlist else None for anyentry in self.worldgdf['iso_a3']]
        self.worldgdf['randomvals'], self.worldgdf['randomvals2'] = randomvalslist, randomvalslist2

        #global_conn.close()

    def showMap(self):

        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['randomvals'], cmap = 'viridis', legend = True)
        plt.figure(1)
        self.worldgdf.plot(edgecolor = 'black', column = self.worldgdf['randomvals2'], cmap = 'viridis', legend = True)
        plt.show()

newInstance = doneWithTheEarth()

newInstance.getUserInput()
newInstance.populateRandomData()
newInstance.showMap()