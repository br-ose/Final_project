import geopandas as gpd
import matplotlib.pyplot as plt
import random
import requests
import json
import pandas as pd
import math
from shapely.geometry import Point
import sqlite3
import os.path
from bs4 import BeautifulSoup
import csv

# 1. Ask user for input -done
# 2. convert into coordinates - done
# 3. ask user for time interval - done
# 4. make api call using those coordinates to get temperature and emissions data - done
# 5. create database 
# 6. store data in database 25 items at a time 
# 7. calculate change in average between two time periods 
# 8. calculate r correlation coefficient
# 9. visualize them all?


class funWithTheEarth:

    def __init__(self): # iniates some key variables

        self.coordinatelist = [] # list where all the coordinates for this session are stored
        self.userinputbool = True # variable for the while loop, guess we don't really need this
        self.drawncount = 0 # variable for my old draw25 function
        self.coordMOE = 0.5 # Margin of Error accepted for what is/isn't a different place; right now, anything within 0.5 geographic coordinate degrees of an existing SQL entry is considered the "same place" as the oldest existing entry in that range

        self.startyear = 1901
        self.endyear = 2001

        ### SQLITE3 TIME ###

        self.global_db_name = 'testdb2' # database file name

        def setUpDatabase(db_name): # function that creates/connects us to the SQL database
                path = os.path.dirname(os.path.abspath(__file__))
                conn = sqlite3.connect(path + '/' + db_name)
                cur = conn.cursor()
                return cur, conn

        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/' + self.global_db_name): # if the database doesn't exist yet,

            self.global_cur, self.global_conn = setUpDatabase(self.global_db_name) # make it! (apparently simply calling the setUpDatabase function creates it?)

            self.global_cur.execute("DROP TABLE IF EXISTS Main_Table") # just to be safe, format the database of any existing Main_Table
            self.global_cur.execute("CREATE TABLE Main_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, point_name TEXT, longitude REAL, latitude REAL)")

            print("\nDatabase created!\n") # statement for user to see a new database was created

        else: # if the databse already exists,

            self.global_cur, self.global_conn = setUpDatabase(self.global_db_name) # just connect to it!

            print("\nDatabase already created, using existing database!\n") # statement for user to see they accessed the existing database

    ### END SQLITE3 TIME ###
    # SOMETHING GOT FUCKED OVER HERE WITH THE DATABSE FILE, DEBUG THIS LATER

    def __str__(self):

        return "This is an object of our class we created, man! You can't just print it!\n\nTake a look at our documentation to learn what to do!"
    
    def getemissions(self,coordinates):
    # Get average carbon monoxide emissions across a given country for the past period
    ## Get average recent emissions
    # use fixed full date
        url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin={}&end={}".format(coordinates,start,start)
        results =  requests.get(url)
        results = results.json()
        self.emissionsresults = emissions

## Coordinates must be inputted as a tuple

#   yo i have no idea what this function is for, i trust you tho!
    # def getcountryfromcoords(self,coords,file):
    #     with open(file) as file2:
    #         csv_reader = csv.reader(file2, delimiter=',')
    #         coordlist = []
    #         next(csv_reader)
    #         shortest_distance = None
    #         shortest_distance_coordinates = None
    #         dalist = []
    #         for row in csv_reader:
    #             coordlist.append((float(row[4].strip().strip('"')),float(row[5].strip().strip('"'))))
    #             dalist.append(row)
    #         for coordinate in coordlist:
    #             distance = math.sqrt(((coordinate[0]-coords[0])**2)+((coordinate[1]-coords[1])**2))
    #             if shortest_distance is None or distance < shortest_distance:
    #                 shortest_distance = distance
    #                 shortest_distance_coordinates = coordinate
    #         for country in dalist:
    #             if float(country[4].strip().strip('"')) == shortest_distance_coordinates[0] and float(country[5].strip().strip('"')) == shortest_distance_coordinates[1]:
    #                 return country[2]

    def gettemp(self,country):
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country)   
        results =  requests.get(url)
        results = results.json()

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
    
    def draw25(self, sets_of_25 = 1):

        for num in range(sets_of_25):

            responsevar = requests.get("https://worldpopulationreview.com/world-cities")
            datavar = responsevar.text
            citysoup = BeautifulSoup(datavar, "html.parser")
            citytable = citysoup.find('tbody', class_ = "jsx-2642336383")
            cityentries = citytable.find_all('tr')
            return_list = []
            for anyrow in cityentries[self.drawncount:self.drawncount + 25]:
                cells = anyrow.find_all('td')
                cityname = cells[1].text + ", " + cells[2].text
                return_list += [cityname]
                self.secondPart(cityname)
            self.drawncount += 25
            print("Attempted to add the following cities to the database: {}".format(str(return_list)))
  
        return return_list
    
    def inputSomeStuff(self): # function for users to input place names

        accum = 0 # number of times user has input data

        while self.userinputbool: # initiate indefinite loop

            if accum <= 24: # if user has entered data 24 times or less,

                userinput = input("Enter a place name to find its coordinates, or type 'exit' to stop adding to the place name list: ") # ask them to enter data

                if userinput.lower() == 'exit' and len(self.coordinatelist) >= 1: # if they type 'exit' and there's data in self.coordinatelist,

                    self.userinputbool = False # end the indefinite loop
                    break 

                elif userinput.lower() == 'exit' and len(self.coordinatelist) == 0: # if they type 'exit' and there's no data in self.coordinatelist,

                    print("\nHey, you have to input at least one place to get this program to work, man!\n\nPlease, give me a place!\n") # ask the user to input data
                    continue # restart the loop

                self.secondPart(userinput) # if neither of the above scenarios occur, run the main data acquisition function on the user's input
                accum += 1 # acknowledge that we added one datum to the templist

            else: # if the user has requested data 25 times,

                print("\nNo more data can be entered this round!\n") # tell them no
                break

        workingbool = True
        
        while workingbool:

            if not workingbool:

                break

            userinput2 = input("Yo, so uh...you wanna see some temp change data? Gimme a starting year between 1901 and 2012 for the range you want: ")

            if userinput2.isdigit() and len(userinput2) == 4 and int(userinput2) >= 1901 and int(userinput2) <= 2012:

                self.startyear = int(userinput2)
                workingbool = False
            
            else:

                print("\nHeyo, uhh...that's not a valid year, chief: gimme a year between 1901 and 2012.\n")
                continue

        workingbool = True
        
        while workingbool:

            if not workingbool:

                break

            userinput3 = input("How about the end year? Gimme one: ")

            if userinput3.isdigit() and len(userinput3) == 4 and int(userinput3) >= 1901 and int(userinput3) <= 2012 and int(userinput3) > int(userinput2):

                self.endyear = int(userinput3)
                workingbool = False
            
            else:

                print("\nHeyo, uhh...that's not a valid year, chief: gimme a year between 1901 and 2012 AFTER your first input year.\n")
                continue

    def secondPart(self, userinput): # aight here's the main func of this badboi

        self.global_cur.execute("SELECT point_name FROM Main_Table") # get all the names from the SQL database
        name_list = [anyentry[0] for anyentry in self.global_cur.fetchall()] # put em in name_list

        if userinput in name_list: # if the userinput is already in the database,

            self.global_cur.execute("SELECT longitude, latitude FROM Main_Table WHERE point_name = ?", (userinput,)) # get the coordinates for it from the database
            userinput_coordinates = self.global_cur.fetchone() 

            coordfoundbool1 = False

            for anycoord in self.coordinatelist: # if the aforementioned coordinates are within 0.5 degrees of any coordinates entered this session,

                if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):

                    coordfoundbool1 = True
                    print("\nYou've already added this place this session!\n\nPlease add a different place, or type 'exit' to stop adding to the place name list.\n") # let the user know they've already added this place to this data entry session

            if not coordfoundbool1: # else, add the coordinates to this session and acknowledge the name match

                self.coordinatelist += [userinput_coordinates]
                print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via name match]\n")

        else: # if the userinput string isn't already in the database,

            requestvar = requests.get("https://open.mapquestapi.com/geocoding/v1/address?key=XGcPnAqF2wxYdwEXRCbUd8vj6G3eAIdg&location={}".format(userinput).replace(" ", "+")) # get the coordinates for that place from the internet
            datavar = json.loads(requestvar.text)
            userinput_coordinates = (float(datavar['results'][0]['locations'][0]['latLng']['lng']), float(datavar['results'][0]['locations'][0]['latLng']['lat']))
            self.global_cur.execute("SELECT longitude, latitude FROM Main_Table") # also get the coordinates in the database
            db_coord_list = self.global_cur.fetchall()

            coordfoundbool3 = False

            for anycoord in self.coordinatelist: # if the user's already added coordinates within 0.5 degrees of their most recent input to this session,

                if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):

                    coordfoundbool3 = True
                    print("\nYou've already added this place this session!\n\nPlease add a different place, or type 'exit' to stop adding to the place name list.\n") # let the user know they've already added this place to this data entry session

            if not coordfoundbool3: # if the user hasn't already added similar coordinates this sessioon,

                coordfoundbool2 = False

                for anycoord in db_coord_list: # see if the coordinates are in the database
                #                       39.5 + 1 = 40.5             40                  39.5 - 1 = 38.5            
                    if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                    and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                    and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                    and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):
                    #if userinput_coordinates in db_coord_list:
                    # if the coordinates aren't already in the database:
                        self.coordinatelist += [userinput_coordinates] # if they are, add them to this session but don't create a new database entry
                        print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via coordinate match]\n")
                        coordfoundbool2 = True
                        
                if not coordfoundbool2: # but, if these coordinates really are brand spankin new,

                    self.global_cur.execute("INSERT INTO Main_Table (point_name, longitude, latitude) VALUES (?, ?, ?)", (userinput, userinput_coordinates[0], userinput_coordinates[1])) # add them to both the database and the templist for this session
                    self.coordinatelist += [userinput_coordinates]
                    self.global_conn.commit()
                    print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [new coordinates added to database]\n")

    ### OKAY THIS IS THE REAL END OF SQLITE3 TIME ###

    def showMeTheMoney(self): # this function produces the map visualization with data from self.inputSomeStuff

        self.global_conn.close() # closes the connection to the database before doing anything, cause we don't need that bad boi hangin around do we

        datapath = gpd.datasets.get_path('naturalearth_lowres') # sets map we're using to a default map of the whole world
        worldgdf = gpd.read_file(datapath)

        newseries = gpd.GeoSeries(Point(self.coordinatelist[0])) # initiates a Pandas series (basically a column for a fancy data table object called a DataFrame)

        for anycoordinates in self.coordinatelist[1:]:
            newseries = newseries.append(gpd.GeoSeries(Point(anycoordinates)), ignore_index = True) # adds the self.coordinateslist coordinates to this new series, all the while processing the coordinates into shapely.geometry Points to use on our map

        dfdict = {'secondseries': [random.randint(1,100) for anyentry in list(newseries)], 'thirdseries': [1 for anyentry in list(newseries)]}

        workingdataframe = pd.DataFrame(dfdict)

        print(workingdataframe)

        pointsgdf = gpd.GeoDataFrame(workingdataframe, geometry = newseries) # creates a GeoPandas DataFrame with both our coordinates and our data
        print(pointsgdf)

        worldplot1 = worldgdf.plot(color='grey', edgecolor='black') # sets colors of the countries/their borders
        pointsgdf.plot(ax=worldplot1, cmap = 'viridis', column = 'secondseries', legend = True, edgecolor = 'black', markersize = 50) # sets the plot's map to the argument ax, chooses a color scheme with the argument cmap, chooses a dataframe column to visualize data from with the column argument, shows us a legend for that data/color scheme when we set the legend arg to True, changes marker size/edge color with those respective arguments
        plt.title('Some cool climate change data (mol/m^3)') # gives our map a title
        plt.xlabel('Longitude') # name the x and y axes,
        plt.ylabel('Latitude')
        plt.figure(1)

        worldplot2 = worldgdf.plot(color = 'grey', edgecolor = 'black')
        pointsgdf.plot(ax=worldplot2, cmap = 'viridis', column = 'thirdseries', legend = True, edgecolor = 'black', markersize = 50)
        plt.title('Temperature change from {} to {}'.format(str(self.startyear), str(self.endyear)))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show() # and poop out a window with our map on it!

        # HOW TO CHANGE POINT SIZE DYNAMICALLY https://gis.stackexchange.com/questions/241612/change-marker-size-in-plot-with-geopandas

newInstance = funWithTheEarth()

#print(newInstance)
newInstance.draw25(4)
#newInstance.inputSomeStuff()
newInstance.showMeTheMoney()