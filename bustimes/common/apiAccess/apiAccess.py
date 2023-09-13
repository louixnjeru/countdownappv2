import json,requests
from .sanitiseData import Sanitiser

class API:
    
    def __init__(self):
        self.apiKey = {'app_key' :'c6a9fc6196c948c79075408ead9420fe'}
        self.sanitise = Sanitiser()
        
    def getStopNames(self, query):
        query = query.replace(' ','%20')
        try:
            response = requests.get(f"https://api.tfl.gov.uk/StopPoint/Search?query={query}&modes=bus",params=self.apiKey).json()
            return self.sanitise.sanitiseStationList(response)
        except response.get('httpStatusCode', None) == 400:
            return False
    
    def getStopsById(self, stopPointId):
        try:
            response = requests.get(f"https://api.tfl.gov.uk/StopPoint/{stopPointId}",params=self.apiKey).json()
            return self.sanitise.sanitiseStopList(response)
        except response.get('httpStatusCode', None) == 400:
            return False
        
    def getArrivalsForStop(self, stopId):
        try:
            response = requests.get(f"https://api.tfl.gov.uk/StopPoint/{stopId}/Arrivals",params=self.apiKey).json()
            return self.sanitise.sanitiseArrivals(response) 
        except response.get('httpStatusCode', None) == 400:
            return False
        
    def getNearestBusStops(self, currLat, currLon):
        try:
            response = requests.get(f"https://api.tfl.gov.uk/StopPoint/?lat={currLat}&lon={currLon}&stopTypes=NaptanPublicBusCoachTram&radius=800&modes=bus").json()
            return self.sanitise.getNearestBusStops(response)
        except response.get('httpStatusCode', None) == 400:
            return False
        
    def getVehicleInfo(self, vehicle, destination):
        response = requests.get(f"https://api.tfl.gov.uk/Vehicle/{vehicle}/Arrivals",params=self.apiKey).json()
        sanitisedResponse = self.sanitise.sanitiseVehicle(response, destination)
        return False if len(sanitisedResponse) == 0 else sanitisedResponse
        
    