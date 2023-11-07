from random import randint


class House:
    def __init__(self, n):
        self.n_people = n
        self.demand = self.__update_demand()

    def update_n_people(self, x):
        if self.n_people + x >= 2:
            self.n_people += x
            self.__update_demand()

    def __update_demand(self):
        self.demand = self.n_people * 100
        return self.demand

    def get_n_people(self):
        return self.n_people

    def get_demand(self):
        return self.demand


class Neighborhood:
    def __init__(self):
        houses = [House(randint(2, 7)) for _ in range(randint(8, 12))]
        self.houses = houses
        self.hospitals = Hospital(houses)
        self.schools = School(houses)
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand()
        self.demand += self.hospitals.get_demand()
        self.demand += self.schools.get_demand()
        return self.demand

    def get_n_houses(self):
        return len(self.houses)

    def get_houses_demand(self):
        return sum([house.get_demand() for house in self.houses])

    def get_demand(self):
        return self.demand

    def __str__(self):
        house_strings = [f'House {i + 1} - Demand={house.get_demand()}' for i, house in enumerate(self.houses)]
        return '\n'.join(house_strings) + f'\n\nHospital - Demand={self.hospitals.get_demand()}\nSchool - Demand={self.schools.get_demand()}\n\nTotal = {self.get_demand()}\n\n'


class Hospital:
    def __init__(self, houses_in_neighborhood):
        self.houses = houses_in_neighborhood
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand() / 2
        return self.demand

    def get_demand(self):
        return self.demand


class School:
    def __init__(self, houses_in_neighborhood):
        self.houses = houses_in_neighborhood
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_n_people() - 2
        return self.demand

    def get_demand(self):
        return self.demand


class EmergencyStation:
    def __init__(self, neighborhoods):
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand()/2
        return self.demand

    def get_demand(self):
        return self.demand


class City:
    def __init__(self, name):
        self.name = name
        self.neighborhoods = [Neighborhood() for _ in range(randint(2, 5))]
        if len(self.neighborhoods) > 3:
            stations_number = 4
        else:
            stations_number = 2
        self.stations = [EmergencyStation(self.neighborhoods) for _ in range(stations_number)]
        self.demand = self.__update_demand()
        self.generation = self.__update_generation()

    def __update_demand(self):
        demand = 0
        for neighborhood in self.neighborhoods:
            demand += neighborhood.get_demand()
        for station in self.stations:
            demand += station.get_demand()
        return demand

    def get_demand(self):
        return self.demand

    def __update_generation(self):
        generation = 0
        return generation

    def get_generation(self):
        return self.generation

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_stations(self):
        return self.stations

    def __str__(self):
        neighborhood_strings = [f'Neighborhood {i + 1}:\n{neighborhood}' for i, neighborhood in enumerate(self.neighborhoods)]
        station_strings = [f'Emergency services {i + 1} - Demand={station.get_demand()}' for i, station in enumerate(self.stations)]
        total_demand = sum(neighborhood.get_demand() for neighborhood in self.neighborhoods) + sum(station.get_demand() for station in self.stations)

        return f'{self.name}\n\n' + '\n'.join(neighborhood_strings) + '\n' + '\n'.join(station_strings) + f'\nTotal Demand = {total_demand}'
