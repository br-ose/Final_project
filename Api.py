import requests


def getemissions(country,start,end):
    ### formatting for start end and coords
    ## yy-mm-dd
    ###x.x,y.y
    # Get the average emissions for a given interval in an area
    url = "https://api.v2.emissions-api.org/api/v2/carbonmonoxide/average.json?country={}&begin={}&end={}".format(country,start,end)
    results =  requests.get(url)
    results = results.json()
    print(results)
    
##Test get emissions
getemissions("USA","2020-01-01","2020-12-01")

def gettemp(country):
    #temp is in celcius

    url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/{}".format(country)   
    results =  requests.get(url)
    results = results.json()
    print(results)

#gettemp("USA")


