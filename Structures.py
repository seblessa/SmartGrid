import random


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


class Neighborhood:
    def __init__(self):
        houses = [House(random.randint(2, 7)) for _ in range(random.randint(8, 12))]
        self.houses = houses
        self.hospitals = Hospital(houses)
        self.schools = School(houses)
        self.demand = self.__update_demand()
        self.generation = 0

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand()
        self.demand += self.hospitals.get_demand()
        self.demand += self.schools.get_demand()
        return self.demand

    def __update_generation(self, increase):
        self.generation += increase

    def get_n_houses(self):
        return len(self.houses)

    def get_houses_demand(self):
        return sum([house.get_demand() for house in self.houses])

    def get_demand(self):
        return self.demand

    def __str__(self):
        house_strings = [f'House {i + 1} - Demand={house.get_demand()}' for i, house in enumerate(self.houses)]
        return '\n'.join(
            house_strings) + f'\n\nHospital - Demand={self.hospitals.get_demand()}\nSchool - Demand={self.schools.get_demand()}\n\nTotal = {self.get_demand()}\n\n'


class PoliceDepartment:
    def __init__(self, neighborhoods):
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 2
        return self.demand

    def get_demand(self):
        return self.demand


class FireDepartment:
    def __init__(self, neighborhoods):
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 3
        return self.demand

    def get_demand(self):
        return self.demand


class WindEnergyStation:
    def __init__(self):
        self.generation = 0
        self.conditions = [
            ("Not generating", 2), ("Not favorable", 5), ("Mildly favorable", 4),
            ("Favorable", 3), ("Very favorable", 2), ("Maximum generation", 1)
        ]
        self.current_condition_index = 0

    def get_generation(self):
        return self.generation

    def refresh(self):
        previous_index = max(0, self.current_condition_index - 1)
        next_index = min(len(self.conditions) - 1, self.current_condition_index + 1)

        previous_weight = self.conditions[previous_index][1]
        next_weight = self.conditions[next_index][1]

        # Generate a random choice based on the weights
        choices = [previous_index, next_index]
        selected_index = random.choices(choices, [previous_weight, next_weight])[0]

        self.current_condition_index = selected_index
        condition, _ = self.conditions[self.current_condition_index]

        if condition == "Not generating":
            self.generation = 0
        elif condition == "Not favorable":
            self.generation = 150
        elif condition == "Mildly favorable":
            self.generation = 300
        elif condition == "Favorable":
            self.generation = 450
        elif condition == "Very favorable":
            self.generation = 600
        elif condition == "Maximum generation":
            self.generation = 750


class SolarEnergyStation:
    def __init__(self):
        self.generation = 100

    def get_generation(self):
        return self.generation

    def refresh(self, time):
        day, weekday, day_or_night = time
        if day_or_night == "day":
            self.generation = 0
        else:
            self.generation = 100


class HydroEnergyStation:
    def __init__(self):
        self.generation = 25000

    def get_generation(self):
        return self.generation

    def refresh(self, time):
        day, weekday, day_or_night = time
        if weekday == "Tuesday" or weekday == "Friday":
            self.generation = 20
        else:
            self.generation = 25000


class FossilFuelEnergyStation:
    def __init__(self):
        self.generation = 0

    def get_generation(self):
        return self.generation

    def update_generation(self, balance):
        self.generation = -1 * balance


class City:
    def __init__(self, name):
        self.name = name

        self.neighborhoods = [Neighborhood() for _ in range(random.randint(3, 5))]
        self.policeDepartments = [PoliceDepartment(self.neighborhoods) for _ in
                                  range((len(self.neighborhoods) // 3) + 1)]
        self.fireDepartments = [FireDepartment(self.neighborhoods) for _ in range((len(self.neighborhoods) // 4) + 1)]
        self.demand = self.__update_demand()

        self.WindEnergyStations = [WindEnergyStation() for _ in range(random.randint(1, 3))]
        self.windGeneration = sum(windStation.generation for windStation in self.WindEnergyStations)
        self.SolarEnergyStations = [SolarEnergyStation() for _ in range(random.randint(50, 100))]
        self.solarGeneration = sum(solarStation.generation for solarStation in self.SolarEnergyStations)
        self.HydroEnergyStation = HydroEnergyStation()
        self.hydroGeneration = self.HydroEnergyStation.get_generation()
        self.FossilFuelEnergyStation = FossilFuelEnergyStation()
        self.fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()
        self.generation = self.windGeneration + self.solarGeneration + self.hydroGeneration + self.fossilFuelGeneration

    def __update_demand(self):
        demand = 0
        for neighborhood in self.neighborhoods:
            demand += neighborhood.get_demand()
        for police in self.policeDepartments:
            demand += police.get_demand()
        for fire in self.fireDepartments:
            demand += fire.get_demand()
        return demand

    def get_demand(self):
        return self.demand

    def get_generation(self, current_time):
        for windEnergyStation in self.WindEnergyStations:
            windEnergyStation.refresh()
            self.windGeneration += windEnergyStation.get_generation()
        for solarEnergyStation in self.SolarEnergyStations:
            solarEnergyStation.refresh(current_time)
            self.solarGeneration += solarEnergyStation.get_generation()

        self.HydroEnergyStation.refresh(current_time)
        self.hydroGeneration = self.HydroEnergyStation.get_generation()

        self.FossilFuelEnergyStation.update_generation(self.get_balance())
        self.fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()

        self.generation = self.windGeneration + self.solarGeneration + self.hydroGeneration + self.fossilFuelGeneration

        return self.generation

    def get_balance(self):
        return self.generation - self.demand

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_police_department(self):
        return self.policeDepartments

    def get_fire_department(self):
        return self.fireDepartments

    def __str__(self):
        neighborhood_strings = [f'Neighborhood {i + 1} - Demand={neighborhood.get_demand()}' for i, neighborhood in
                                enumerate(self.neighborhoods)]
        police_strings = [f'Police Department {i + 1} - Demand={police.get_demand()}' for i, police in
                          enumerate(self.policeDepartments)]
        fire_string = [f'Fire Department {i + 1} - Demand={fire.get_demand()}' for i, fire in
                       enumerate(self.fireDepartments)]
        total_demand = sum(neighborhood.get_demand() for neighborhood in self.neighborhoods) + sum(
            police.get_demand() for police in self.policeDepartments) + sum(
            fire.get_demand() for fire in self.fireDepartments)

        windStation_string = [f'Wind Station {i + 1} - Generation={wind.get_generation()}' for i, wind in
                              enumerate(self.WindEnergyStations)]
        solarStation_string = [f'{len(self.SolarEnergyStations)} solar panels - Generation={self.solarGeneration}']
        hydroStation_string = [f'Hydro Station - Generation={self.hydroGeneration}']
        ffStation_string = [f'Fossil Fuel - Generation={self.fossilFuelGeneration}']

        total_generation = (sum(windStation.get_generation() for windStation in self.WindEnergyStations) + sum(
            solarStation.get_generation() for solarStation in self.SolarEnergyStations) +
                            self.hydroGeneration + self.fossilFuelGeneration)

        return ('\n'.join(neighborhood_strings) + '\n' +
                '\n'.join(police_strings) + '\n' +
                '\n'.join(fire_string) + '\n' +
                f'\nTotal Demand = {total_demand}\n\n' +
                '\n'.join(windStation_string) + '\n' +
                '\n'.join(solarStation_string) + '\n' +
                '\n'.join(hydroStation_string) + '\n' +
                '\n'.join(ffStation_string) + '\n' +
                f'\nTotal Generation = {total_generation}\n\n' +
                f'Balance = {self.get_balance()}')

