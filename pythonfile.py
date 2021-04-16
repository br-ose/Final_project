import geopandas as gpd
import matplotlib.pyplot as plt
import random
import requests
import json
import pandas as pd
from shapely.geometry import Point

userinput = input("Enter a place name to find its coordinates: ")
requestvar = requests.get("https://open.mapquestapi.com/geocoding/v1/address?key=XGcPnAqF2wxYdwEXRCbUd8vj6G3eAIdg&location={}".format(userinput).replace(" ", "+"))
datavar = json.loads(requestvar.text)
userinput_coordinates = (float(datavar['results'][0]['locations'][0]['latLng']['lat']), float(datavar['results'][0]['locations'][0]['latLng']['lng']))
print("Your coordinates are " + str(userinput_coordinates))

#datapath = gpd.datasets.get_path('naturalearth_lowres')
worlddata = gpd.read_file('cb_2018_us_state_5m.shx')
#data = data.set_index('BoroName')

#worlddata = worlddata[(worlddata.pop_est > 0) & (worlddata.name != "Antarctica")]

newseries = gpd.GeoSeries(Point((userinput_coordinates[1], userinput_coordinates[0])))
#finalgdf = worlddata.geometry.append(newgdf)

joinedgdf = gpd.GeoDataFrame(geometry = worlddata.geometry.append(newseries, ignore_index = True))

#finalgdf = gpd.GeoDataFrame(pd.concat([worlddata, newgdf], ignore_index=True), crs=worlddata.crs)

print(joinedgdf)

#worlddata['random_data'] = list(range(176)) # this is how we can add data to the GeoDataFrame

#country_index_dict = {worlddata.name[number]: worlddata.index[number] for number in range(176) if number != 159} # me creating a dictionary with country names and corresponding index numbers, which are seemingly random
#print(country_index_dict)

#print(worlddata.index["Afghanistan"])

joinedgdf.plot(cmap = 'gist_rainbow')

#tennisdict = {'Novak Djokovic': 2, 'Naomi Osaka': 2, 'Rafael Nadal': 1, 'Iga Świątek': 1, 'Simona Halep': 1, 'Dominic Thiem': 1}
#plt.bar(list(tennisdict.keys()),list(tennisdict.values()))

#worlddata.boundary.plot()
plt.show()