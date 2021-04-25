import geopandas as gpd
import matplotlib.pyplot as plt
#import random
import requests
import json
import pandas as pd
import math
from shapely.geometry import Point
import sqlite3
import os.path
from bs4 import BeautifulSoup

# 1. Ask user for input
# 2. convert into coordinates
# 3. ask user for time interval
# 4. make api call using those coordinates to get temperature and emissions data 
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

            print("Database already created!")
    ### END SQLITE3 TIME ###
    # SOMETHING GOT FUCKED OVER HERE WITH THE DATABSE FILE, DEBUG THIS LATER

    def __str__(self):

        return "This is an object of our class we created, man! You can't just print it!\n\nTake a look at our documentation to learn what to do!"
    
    def getemissions(self,coordinates,start,end):
    # Get average carbon monoxide emissions across a given country for the past period
        url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin={}&end={}".format(country,start,end)
        results =  requests.get(url)
        results = results.json()
        self.emissionsresults = emissions

## Coordinates must be inputted as a tuple
    def getcountryfromcoords(self,coords,file):
        with open(file) as file2:
            csv_reader = csv.reader(file2, delimiter=',')
            coordlist = []
            next(csv_reader)
            shortest_distance = None
            shortest_distance_coordinates = None
            dalist = []
            for row in csv_reader:
                coordlist.append((float(row[4].strip().strip('"')),float(row[5].strip().strip('"'))))
                dalist.append(row)
            for coordinate in coordlist:
                distance = math.sqrt(((coordinate[0]-coords[0])**2)+((coordinate[1]-coords[1])**2))
                if shortest_distance is None or distance < shortest_distance:
                    shortest_distance = distance
                    shortest_distance_coordinates = coordinate
            for country in dalist:
                if float(country[4].strip().strip('"')) == shortest_distance_coordinates[0] and float(country[5].strip().strip('"')) == shortest_distance_coordinates[1]:
                    return country[2]

    def gettemp(self,coordinates):
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country)   
        results =  requests.get(url)
        results = results.json()
        self.tempresults = results

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

    def secondPart(self, userinput): # aight here's the main func of this badboi

        self.global_cur.execute("SELECT point_name FROM Main_Table")
        name_list = [anyentry[0] for anyentry in self.global_cur.fetchall()]

        if userinput in name_list:

            self.global_cur.execute("SELECT longitude, latitude FROM Main_Table WHERE point_name = ?", (userinput,))
            userinput_coordinates = self.global_cur.fetchone()

            coordfoundbool1 = False

            for anycoord in self.coordinatelist:

                if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):

                    coordfoundbool1 = True
                    print("\nYou've already added this place this session!\n\nPlease add a different place, or type 'exit' to stop adding to the place name list.\n")

            if not coordfoundbool1:

                self.coordinatelist += [userinput_coordinates]
                print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via name match]\n")

        else:

            requestvar = requests.get("https://open.mapquestapi.com/geocoding/v1/address?key=XGcPnAqF2wxYdwEXRCbUd8vj6G3eAIdg&location={}".format(userinput).replace(" ", "+"))
            datavar = json.loads(requestvar.text)
            userinput_coordinates = (float(datavar['results'][0]['locations'][0]['latLng']['lng']), float(datavar['results'][0]['locations'][0]['latLng']['lat']))
            self.global_cur.execute("SELECT longitude, latitude FROM Main_Table")
            db_coord_list = self.global_cur.fetchall()

            coordfoundbool3 = False

            for anycoord in self.coordinatelist:

                if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):

                    coordfoundbool3 = True
                    print("\nYou've already added this place this session!\n\nPlease add a different place, or type 'exit' to stop adding to the place name list.\n")

            if not coordfoundbool3:

                coordfoundbool2 = False

                for anycoord in db_coord_list:
                #                       39.5 + 1 = 40.5             40                  39.5 - 1 = 38.5            
                    if (anycoord[0] <= userinput_coordinates[0] + self.coordMOE 
                    and anycoord[0] >= userinput_coordinates[0] - self.coordMOE 
                    and anycoord[1] <= userinput_coordinates[1] + self.coordMOE
                    and anycoord[1] >= userinput_coordinates[1] - self.coordMOE):
                    #if userinput_coordinates in db_coord_list:
                    # if the coordinates aren't already in the database:
                        self.coordinatelist += [userinput_coordinates]
                        print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via coordinate match]\n")
                        coordfoundbool2 = True
                        
                if not coordfoundbool2:

                    self.global_cur.execute("INSERT INTO Main_Table (point_name, longitude, latitude) VALUES (?, ?, ?)", (userinput, userinput_coordinates[0], userinput_coordinates[1]))
                    self.coordinatelist += [userinput_coordinates]
                    self.global_conn.commit()
                    print("\nAdded your coordinates, " + str(userinput_coordinates) + ", to templist! [new coordinates added to database]\n")

    ### OKAY THIS IS THE REAL END OF SQLITE3 TIME ###

    def showMeTheMoney(self):

        self.global_conn.close()

        datapath = gpd.datasets.get_path('naturalearth_lowres')
        worldgdf = gpd.read_file(datapath)

        #worlddata = worlddata[(worlddata.pop_est > 0) & (worlddata.name != "Antarctica")]

        newseries = gpd.GeoSeries(Point(self.coordinatelist[0]))

        #seriesofnumbers = pd.Series(list(range(len())))

        for anycoordinates in self.coordinatelist[1:]:
            newseries = newseries.append(gpd.GeoSeries(Point(anycoordinates)), ignore_index = True)

        #joinedgdf = gpd.GeoDataFrame(geometry = worlddata.geometry.append(newseries, ignore_index = True))

        #print(joinedgdf)

        #worlddata['random_data'] = list(range(176)) # this is how we can add data to the GeoDataFrame

        #country_index_dict = {worlddata.name[number]: worlddata.index[number] for number in range(176) if number != 159} # me creating a dictionary with country names and corresponding index numbers, which are seemingly random
        #print(country_index_dict)

        #print(worlddata.index["Afghanistan"])

        #joinedgdf.plot(cmap = 'Dark2')
        #pointdata = gpd.GeoDataFrame(geometry = newseries)
        #pointdata.plot(cmap = 'gist_rainbow')

        #tennisdict = {'Novak Djokovic': 2, 'Naomi Osaka': 2, 'Rafael Nadal': 1, 'Iga Świątek': 1, 'Simona Halep': 1, 'Dominic Thiem': 1}
        #plt.bar(list(tennisdict.keys()),list(tennisdict.values()))

        #worlddata.boundary.plot()

        print(list(newseries))

        iterator = 1
        secondseries = pd.Series([iterator])
        #iterator = 1

        for anyitem in list(newseries)[1:]:
            iterator += 1
            if iterator <= 101:
                secondseries = secondseries.append(pd.Series([iterator]), ignore_index = True)
            else:
                secondseries = secondseries.append(pd.Series([101]), ignore_index = True)

        secondseries = secondseries.rename('secondseries')

        print(list(secondseries))


        pointsgdf = gpd.GeoDataFrame(secondseries, geometry = newseries)
        print(pointsgdf)
        #pointsgdf['newcolumn'] = []
        #pointsgdf.assign(newcolumn = random.randint(1,100))
        #for anyentry in pointsgdf['geometry']:
        #    pointsgdf['newcolumn'] += [random.randint(1,100)]

        worldplot = worldgdf.plot(color='grey', edgecolor='black')
        #worldplot.set_axis_bgcolor("#OFOFOF")
        pointsgdf.plot(ax=worldplot, cmap = 'viridis', column = 'secondseries', legend = True, edgecolor = 'black', markersize = 50) # column = 'newcolumn' scheme = 'quantiles'
        #plt.legend(loc='best')
        plt.title('Some cool climate change data (mol/m^3)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

        # HOW TO CHANGE POINT SIZE DYNAMICALLY https://gis.stackexchange.com/questions/241612/change-marker-size-in-plot-with-geopandas

newInstance = funWithTheEarth()

#print(newInstance)
#newInstance.draw25(4)
newInstance.inputSomeStuff()
newInstance.showMeTheMoney()
#for anyentry in newInstance.draw25():
    #print(str(anyentry) + '\n\n')