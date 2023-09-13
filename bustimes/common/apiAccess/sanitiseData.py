class Sanitiser:
    
    def checkAdditionalProperties(self, stop):
        if len(stop["additionalProperties"]) == 0:
            return " "
        elif len(stop["additionalProperties"]) > 1 and stop["additionalProperties"][1]["key"] == "Towards":
            return stop["additionalProperties"][1]["value"]
        else:
            return stop["additionalProperties"][0]["value"]
        
    def sanitiseStopList(self, station):
        name = station['commonName']
        stops = self.findBusStops(station)
        
        return name, stops
    
    def findBusStops(self, station):
        stopList = []
        if "children" in station and len(station["children"]) > 0:
            for child in station["children"]:
                    stopList += self.findBusStops(child)
        if station["stopType"] == "NaptanPublicBusCoachTram" and len(station["lineModeGroups"]) != 0:
            stopList.append({
                "id" : station["naptanId"],
                "name" : station["commonName"],
                "stopLetter" : station["stopLetter"] if "stopLetter" in station else None,
                "routes" : station["lineModeGroups"][0]["lineIdentifier"],
                "waypoint" : self.checkWaypoint(self.checkAdditionalProperties(station), False)
                })
        
        return stopList
    
    def getNearestBusStops(self, stationList):
        stopList = []
        for station in stationList['stopPoints']:
            if station["stopType"] == "NaptanPublicBusCoachTram" and len(station["lineModeGroups"]) != 0:
                stopList.append({
                    "id" : station["naptanId"],
                    "name" : station["commonName"],
                    "stopLetter" : station["stopLetter"] if "stopLetter" in station else None,
                    "routes" : station["lineModeGroups"][0]["lineIdentifier"],
                    "waypoint" : self.checkWaypoint(self.checkAdditionalProperties(station), False)
                    })
        
        return stopList
            
    
    def sanitiseStationList(self, stationList):
        matches, stops = stationList['total'], []
        
        for stop in stationList['matches']:
            stops.append({'name': stop['name'], 'id': stop['id']})
            
        return (matches, stops)
    
    def sanitiseArrivals(self, busTimes):
        arrivalsList = []
        
        if len(busTimes) > 0:
            busTimes.sort(key=lambda x: x['timeToStation'])
            
            for entry in busTimes:
                arrivalsList.append({
                    "destination" : entry["destinationName"],
                    "bearing" : entry["bearing"],
                    "direction" : entry["direction"],
                    "waypoint" : self.checkWaypoint(entry["towards"],True),
                    "route" : entry["lineName"],
                    "stopSign" : self.checkStopName(entry["platformName"]),
                    "stopId" : entry["naptanId"],
                    "stopName" : entry["stationName"],
                    "dueSeconds" : entry["timeToStation"],
                    "due" : self.calculateTime(entry["timeToStation"]),
                    "vehicleId" : entry["vehicleId"]
                    })
                
        return arrivalsList
    
    def sanitiseVehicle(self, vehicle, destination):
        vehicleTimes = []
        if len(vehicle) == 0: return vehicleTimes
        for stop in vehicle:
            if stop['destinationName'] == destination:
                vehicleTimes.append({
                    'id': stop['naptanId'],
                    'route': stop['lineName'],
                    'name': stop['stationName'],
                    'stopLetter': stop['platformName'],
                    'waypoint': stop['towards'],
                    'dueSeconds': stop['timeToStation'],
                    'due': self.calculateTime(stop["timeToStation"]),
                    })
        
        return vehicleTimes
        
    
    def checkWaypoint(self, waypoint, newLine):
        if waypoint[0:10] == 'BikePoints' or waypoint[0:8] == 'TaxiRank':
            return " "
        else:
            return f"Buses towards:\n {waypoint}" if newLine == True else f"Buses towards {waypoint}"

        
    def checkStopName(self, stopName):
        return " "  if stopName == 'null' else stopName
        
    def calculateTime(self, time):
        if time <= 60:
            return "Due"
        elif time > 60 and time <= 120:
            return "1 min"
        else:
            return f"{int(time/60)} mins"