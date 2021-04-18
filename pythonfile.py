import geopandas as gpd
import matplotlib.pyplot as plt
import random
import requests
import json
import pandas as pd
from shapely.geometry import Point

coordinatelist = []
userinputbool = True

while userinputbool:
    userinput = input("Enter a place name to find its coordinates, or type 'exit' to stop adding to the place name list: ")
    if userinput.lower() == 'exit':
        userinputbool = False
        break
    requestvar = requests.get("https://open.mapquestapi.com/geocoding/v1/address?key=XGcPnAqF2wxYdwEXRCbUd8vj6G3eAIdg&location={}".format(userinput).replace(" ", "+"))
    datavar = json.loads(requestvar.text)
    userinput_coordinates = (float(datavar['results'][0]['locations'][0]['latLng']['lng']), float(datavar['results'][0]['locations'][0]['latLng']['lat']))
    coordinatelist += [userinput_coordinates]
    print("Your coordinates are " + str(userinput_coordinates))

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

iterator = 100
secondseries = pd.Series([iterator])
iterator = 1

for anyitem in list(newseries)[1:]:
    iterator += 1
    secondseries = secondseries.append(pd.Series([iterator]), ignore_index = True)

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
pointsgdf.plot(ax=worldplot, cmap = 'viridis', column = 'secondseries', legend = True) # column = 'newcolumn' scheme = 'quantiles'
#plt.legend(loc='best')
plt.title('Some cool climate change data (mol/m^3)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()