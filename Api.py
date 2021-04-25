import requests
import math
import csv

def getcountryfromcoords(coords,file):
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

def gettemp(coordinates):
        country = getcountryfromcoords(coordinates,"countries_codes_and_coordinates.csv")
        print(country)
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country.strip().strip('"'))
        print(url)
        results =  requests.get(url,timeout=5)
        results = results.json()
        tempresults = results
        print(tempresults)

gettemp((24,-76))


