import requests
import math
import csv
import os
import sqlite3

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

def gettemp(coordinates,year1,year2):
        ## Both years should be positive integers and year 2 should be a greater number than year 1
        ### year1 is lower bound year2 is higher one
        ### coordinates is coordinates
        ### Returns the difference
        country = getcountryfromcoords(coordinates,"countries_codes_and_coordinates.csv")
        print(country)
        url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country.strip().rstrip('"').lstrip('"'))
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

def setUpDatabase(db_name):   
     path = os.path.dirname(os.path.abspath(__file__))    
     conn = sqlite3.connect(path+'/'+db_name)    
     cur = conn.cursor()    
     return cur, conn
def createtempdatabase(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS tempdata (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_a3 TEXT, tempchange REAL)")
    conn.commit()
def createemissionsdatabase(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Emissions_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_a3 TEXT, emissions REAL)")
    conn.commit()

def addemissions(cur,conn,country,emissionsresults):
    cur.execute("INSERT INTO Emissions_Data(iso_a3,emissions) VALUES(?,?)",(country,emissionsresults))

def findtopstats(cur,conn):
    cur.execute("SELECT iso_a3,emissions FROM Emissions_Data where emissions = (SELECT MAX(emissions) FROM Emissions_Data)")
    highest = cur.fetchall()
    cur.execute("SELECT iso_a3,emissions FROM Emissions_Data where emissions = (SELECT MIN(emissions) FROM Emissions_Data)")
    lowest = cur.fetchall()
    print(highest)
    print(lowest)
    #cur.execute("SELECT Emissions_Data.emissions")
    
    

    
print(gettemp((24,-76),1920,2012))
cur,conn = setUpDatabase("testbase.db")
createtempdatabase(cur,conn)
createemissionsdatabase(cur,conn)
addemissions(cur,conn,"USA",20.0)
addemissions(cur,conn,"RUS",10.0)
addemissions(cur,conn,"DNK",30.0)
findtopstats(cur,conn)
