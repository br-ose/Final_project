import requests
import csv


def getcountrycode(country,file):
    #Asks for the user to give a country and then finds the country code for that country
    with open(file) as file2:
         csv_reader = csv.reader(file2, delimiter=',')
         for row in csv_reader:
             if row[0] == country:
                 return row[2]

def getemissions(country,start,end):
    # Get average carbon monoxide emissions across a given country for the past 1 year period 
    url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin={}&end={}".format(country,start,end)
    results =  requests.get(url)
    results = results.json()
    print(results)
    return results
    
def gettemp(country):
    #temp is in celcius
    # Gets the past
    url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country)   
    results =  requests.get(url)
    results = results.json()
    print(results)

def setup():
    pass
    #Sets up database

def addtemp(tempdata):
    ## adds the temp data to the database in chunks
    #Shared key is country
    pass
def addemissions(emdata):
    # adds emissions data in chunks
    #Shared key is country
    pass
def calculateavg():
    # gets the average emissions of a country and compares 
    pass

getcountrycode("United States","countries_codes_and_coordinates.csv")
##Test get emissions
#getemissions("USA","2020-01-01","2020-12-31")
#Test get temp
gettemp("USA")


