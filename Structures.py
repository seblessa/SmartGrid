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
    def __init__(self, houses):
        self.houses = houses
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand()
        return self.demand

    def get_houses(self):
        return self.houses

    def get_demand(self):
        return self.demand

    def __str__(self):
        house_strings = [f'House {i + 1}: {house.get_n_people()} residents' for i, house in enumerate(self.houses)]
        return '\n'.join(house_strings)


class Hospital:
    def __init__(self, neighborhood):
        self.houses = neighborhood.get_houses()
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand() / 2
        return self.demand

    def get_demand(self):
        return self.demand


class School:
    def __init__(self, neighborhood):
        self.houses = neighborhood.get_houses()
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_n_people() - 2 * 50
        return self.demand

    def get_demand(self):
        return self.demand


class EmergencyServices:
    def __init__(self, neighborhoods):
        self.neighborhoods = neighborhoods
        self.demand = 250 * len(neighborhoods)

    def get_demand(self):
        return self.demand


class City:
    def __init__(self, name, neighborhoods, schools, hospitals, emergency_services):
        self.name = name
        self.neighborhoods = neighborhoods
        self.schools = schools
        self.hospitals = hospitals
        self.emergency_services = emergency_services

    def get_demand(self):
        demand = 0
        for building in self.neighborhoods:
            demand += building.get_demand()
        for building in self.schools:
            demand += building.get_demand()
        for building in self.hospitals:
            demand += building.get_demand()
        for building in self.emergency_services:
            demand += building.get_demand()
        return demand

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_schools(self):
        return self.schools

    def get_hospitals(self):
        return self.hospitals

    def get_emergency_services(self):
        return self.emergency_services

    def __str__(self):
        return self.name
