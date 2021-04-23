import geopandas as gpd
import matplotlib.pyplot as plt
#import random
import requests
import json
import pandas as pd
from shapely.geometry import Point
import sqlite3
import os.path

coordinatelist = []
userinputbool = True

### SQLITE3 TIME ###

global_db_name = 'testdb2'

def setUpDatabase(db_name):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_name)
        cur = conn.cursor()
        return cur, conn

if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/'+global_db_name):

    global_cur, global_conn = setUpDatabase(global_db_name)

    global_cur.execute("DROP TABLE IF EXISTS Main_Table")
    global_cur.execute("CREATE TABLE Main_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, point_name TEXT, longitude REAL, latitude REAL)")

    print("Database created!")

else:

    global_cur, global_conn = setUpDatabase(global_db_name)

    print("Database already created!")

### END SQLITE3 TIME ###
# SOMETHING GOT FUCKED OVER HERE WITH THE DATABSE FILE, DEBUG THIS LATER

while userinputbool:

    userinput = input("Enter a place name to find its coordinates, or type 'exit' to stop adding to the place name list: ")

    if userinput.lower() == 'exit':

        userinputbool = False
        break

    global_cur.execute("SELECT point_name FROM Main_Table")
    name_list = [anyentry[0] for anyentry in global_cur.fetchall()]

    if userinput in name_list:

        global_cur.execute("SELECT longitude, latitude FROM Main_Table WHERE point_name = ?", (userinput,))
        userinput_coordinates = global_cur.fetchone()
        coordinatelist += [userinput_coordinates]
        print("Added your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via name match]")

    else:

        requestvar = requests.get("https://open.mapquestapi.com/geocoding/v1/address?key=XGcPnAqF2wxYdwEXRCbUd8vj6G3eAIdg&location={}".format(userinput).replace(" ", "+"))
        datavar = json.loads(requestvar.text)
        userinput_coordinates = (float(datavar['results'][0]['locations'][0]['latLng']['lng']), float(datavar['results'][0]['locations'][0]['latLng']['lat']))
        global_cur.execute("SELECT longitude, latitude FROM Main_Table")
        coord_list = global_cur.fetchall()

        if userinput_coordinates in coord_list:
        # if the coordinates aren't already in the database:
            coordinatelist += [userinput_coordinates]
            print("Added your coordinates, " + str(userinput_coordinates) + ", to templist! [coordinates found in database via coordinate match]")
            
        else:

            global_cur.execute("INSERT INTO Main_Table (point_name, longitude, latitude) VALUES (?, ?, ?)", (userinput, userinput_coordinates[0], userinput_coordinates[1]))
            coordinatelist += [userinput_coordinates]
            global_conn.commit()
            print("Added your coordinates, " + str(userinput_coordinates) + ", to templist! [new coordinates added to database]")
            
global_conn.close()

### OKAY THIS IS THE REAL END OF SQLITE3 TIME ###

datapath = gpd.datasets.get_path('naturalearth_lowres')
worldgdf = gpd.read_file(datapath)

#worlddata = worlddata[(worlddata.pop_est > 0) & (worlddata.name != "Antarctica")]

newseries = gpd.GeoSeries(Point(coordinatelist[0]))

#seriesofnumbers = pd.Series(list(range(len())))

for anycoordinates in coordinatelist[1:]:
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
    iterator += 10
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