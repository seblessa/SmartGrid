from Structures import *
import random


class SmartGridEnvironment:
    def __init__(self, city_name="Porto"):
        self.city_name = city_name

        self.current_time = (1, "Monday", "day")

        self.neighborhoods = [Neighborhood() for _ in range(random.randint(3, 5))]
        self.hospital = Hospital(sum([neighborhood.get_houses_demand() for neighborhood in self.neighborhoods]))
        self.policeDepartment = PoliceDepartment(self.neighborhoods)
        self.fireDepartment = FireDepartment(self.neighborhoods)
        self.demand = self.__update_demand()  # TODO - exchange with a setter method activated by an agent

        self.__WindEnergyStations = [WindEnergyStation() for _ in range(random.randint(3, 7))]
        self.__SolarEnergyStations = [SolarEnergyStation() for _ in range(random.choice([16, 25, 36, 49, 64]))]
        self.__HydroEnergyStation = HydroEnergyStation()
        self.FossilFuelEnergyStation = FossilFuelEnergyStation()

        self.__fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()

        self.fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()
        self.__green_generation = 0

    # TODO - functions to keep {
    def get_name(self):
        return self.city_name

    def get_time(self):
        return self.current_time

    def update_time(self):
        day, weekday, day_or_night = self.current_time
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_or_night == "day":
            self.current_time = (day, weekday, "night")
        else:
            self.current_time = (day + 1, days_of_week[(days_of_week.index(weekday) + 1) % len(days_of_week)], "day")
        # self.__update_generation(self.current_time)

    def get_wind_stations(self):
        return self.__WindEnergyStations

    def get_solar_stations(self):
        return self.__SolarEnergyStations

    def get_hydro_station(self):
        return self.__HydroEnergyStation

    def set_green_generation(self, green_generation):
        self.__green_generation = green_generation

    # TODO - }

    # TODO - DELETE AFTER {

    def get_green_generation(self):
        return self.__green_generation

    # TODO - }

    def __update_demand(self):
        demand = 0
        for neighborhood in self.neighborhoods:
            demand += neighborhood.get_demand()
        demand += self.hospital.get_demand()
        demand += self.policeDepartment.get_demand()
        demand += self.fireDepartment.get_demand()
        return demand

    def __update_generation(self, current_time):
        self.windGeneration = 0
        self.solarGeneration = 0
        self.hydroGeneration = 0
        self.fossilFuelGeneration = 0

        for windEnergyStation in self.WindEnergyStations:
            windEnergyStation.refresh()
            self.windGeneration += windEnergyStation.get_generation()
        for solarEnergyStation in self.SolarEnergyStations:
            solarEnergyStation.refresh(current_time)
            self.solarGeneration += solarEnergyStation.get_generation()

        self.HydroEnergyStation.refresh()
        self.hydroGeneration = self.HydroEnergyStation.get_generation()

        self.FossilFuelEnergyStation.get_generation()
        self.fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()

        self.green_generation = self.windGeneration + self.solarGeneration + self.hydroGeneration
        green_generation = self.green_generation

        min_gen = min(self.hospital.get_demand(), green_generation)
        green_generation = max(0, green_generation - min_gen)
        self.hospital.update_generation(min_gen)

        min_gen = min(self.policeDepartment.get_demand(), green_generation)
        green_generation = max(0, green_generation - min_gen)
        self.policeDepartment.update_generation(min_gen)

        min_gen = min(self.fireDepartment.get_demand(), green_generation)
        green_generation = max(0, green_generation - min_gen)
        self.fireDepartment.update_generation(min_gen)

        for neighborhood in self.neighborhoods:
            min_gen = min(neighborhood.get_demand(), green_generation)
            green_generation = max(0, green_generation - min_gen)
            neighborhood.update_generation(min_gen)

    def get_demand(self):
        return self.demand

    def get_balance(self):
        return self.__green_generation + self.__fossilFuelGeneration - self.demand

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_hospital(self):
        return self.hospital

    def get_police_department(self):
        return self.policeDepartment

    def get_fire_department(self):
        return self.fireDepartment

    def get_ff_generation(self):
        return self.fossilFuelGeneration

    def get_ff_station(self):
        return self.FossilFuelEnergyStation

    def update_ff_generation(self):
        if self.get_balance() > 0:
            self.FossilFuelEnergyStation.decrease_generation(self.get_balance())
        else:
            self.FossilFuelEnergyStation.increase_generation(self.get_balance())

    def __str__(self):
        neighborhood_strings = [f'Neighborhood {i + 1} - Demand={neighborhood.get_demand()}' for i, neighborhood in
                                enumerate(self.neighborhoods)]
        hospital_strings = [f'Hospital - Demand={self.hospital.get_demand()}']
        police_strings = [f'Police Department - Demand={self.policeDepartment.get_demand()}']
        fire_string = [f'Fire Department - Demand={self.fireDepartment.get_demand()}']
        total_demand = sum(neighborhood.get_demand() for neighborhood in
                           self.neighborhoods) + self.hospital.get_demand() + self.policeDepartment.get_demand() + self.fireDepartment.get_demand()

        windStation_string = [f'Wind Station {i + 1} - Generation={wind.get_generation()}' for i, wind in
                              enumerate(self.WindEnergyStations)]
        solarStation_string = [f'{len(self.SolarEnergyStations)} solar panels - Generation={self.solarGeneration}']
        hydroStation_string = [f'Hydro Station - Generation={self.hydroGeneration}']
        ffStation_string = [f'Fossil Fuel - Generation={self.fossilFuelGeneration}']

        total_generation = (sum(windStation.get_generation() for windStation in self.WindEnergyStations) + sum(
            solarStation.get_generation() for solarStation in self.SolarEnergyStations) +
                            self.hydroGeneration + self.fossilFuelGeneration)

        return ('\n'.join(neighborhood_strings) + '\n' +
                '\n'.join(hospital_strings) + '\n' +
                '\n'.join(police_strings) + '\n' +
                '\n'.join(fire_string) + '\n' +
                f'\nTotal Demand = {total_demand}\n\n' +
                '\n'.join(windStation_string) + '\n' +
                '\n'.join(solarStation_string) + '\n' +
                '\n'.join(hydroStation_string) + '\n' +
                '\n'.join(ffStation_string) + '\n' +
                f'\nTotal Generation = {total_generation}\n\n' +
                f'Balance = {self.get_balance()}')
