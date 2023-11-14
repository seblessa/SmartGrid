from Structures import *
import random


class SmartGridEnvironment:
    def __init__(self, city_name="Porto"):
        self.city_name = city_name

        self.current_time = (1, "Monday", "day")
        self.generation = 0

        self.neighborhoods = [Neighborhood() for _ in range(random.randint(3, 5))]
        self.policeDepartments = [PoliceDepartment(self.neighborhoods) for _ in
                                  range((len(self.neighborhoods) // 3) + 1)]
        self.fireDepartments = [FireDepartment(self.neighborhoods) for _ in range((len(self.neighborhoods) // 4) + 1)]
        self.demand = self.__update_demand()

        self.WindEnergyStations = [WindEnergyStation() for _ in range(random.randint(3, 5))]
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

        self.HydroEnergyStation.refresh(current_time)
        self.hydroGeneration = self.HydroEnergyStation.get_generation()

        self.FossilFuelEnergyStation.get_generation()
        self.fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()

        self.generation = self.windGeneration + self.solarGeneration + self.hydroGeneration + self.fossilFuelGeneration

    def update_time(self):
        day, weekday, day_or_night = self.current_time
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_or_night == "day":
            self.current_time = (day, weekday, "night")
        else:
            self.current_time = (day + 1, days_of_week[(days_of_week.index(weekday) + 1) % len(days_of_week)], "day")
        self.__update_generation(self.current_time)

    def get_demand(self):
        return self.demand

    def get_generation(self):
        return self.generation

    def get_balance(self):
        return self.generation - self.demand

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_police_department(self):
        return self.policeDepartments

    def get_fire_department(self):
        return self.fireDepartments

    def get_status(self):
        return self.demand, self.generation, self.get_demand() - self.get_generation()

    def get_time(self):
        return self.current_time

    def update_ff_generation(self):
        if self.get_balance() > 0:
            self.FossilFuelEnergyStation.decrease_generation(self.get_balance())
        else:
            self.FossilFuelEnergyStation.increase_generation(self.get_balance())

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
