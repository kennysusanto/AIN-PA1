class City:
    def __init__(self, name, coor):
        self.city_name = name
        self.x = coor[0]
        self.y = coor[1]
        self.connected_cities = {}

    def getCoor(self):
        return [self.x, self.y]

    def getCityName(self):
        return self.city_name
    
    def addConnectedCity(self, destination_city_name, distance):
        self.connected_cities[destination_city_name] = distance

    def getConnectedCities(self):
        return self.connected_cities