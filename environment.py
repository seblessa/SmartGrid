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

        self.__WindTurbines = [WindTurbine() for _ in range(random.randint(3, 7))]
        self.__wind_generation = 0
        self.__SolarPanels = [SolarPanel() for _ in range(random.choice([16, 25, 36, 49, 64]))]
        self.__solar_generation = 0
        self.__HydroEnergyStation = HydroEnergyStation()
        self.__hydro_generation = 0

        self.FossilFuelEnergyStation = FossilFuelEnergyStation()
        self.__fossilFuelGeneration = self.FossilFuelEnergyStation.get_generation()

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

    def get_wind_turbine(self):
        return self.__WindTurbines

    def get_solar_panels(self):
        return self.__SolarPanels

    def get_hydro_generator(self):
        return self.__HydroEnergyStation

    def set_wind_generation(self, wind_generation):
        self.__wind_generation = wind_generation

    def set_solar_generation(self, solar_generation):
        self.__solar_generation = solar_generation

    def set_hydro_generation(self, hydro_generation):
        self.__hydro_generation = hydro_generation

    def get_green_generation(self):
        return self.__wind_generation + self.__solar_generation + self.__hydro_generation

    def get_balance(self):
        return self.get_green_generation() + self.__fossilFuelGeneration - self.demand

    def update_generation(self):
        for windEnergyStation in self.__WindTurbines:
            windEnergyStation.refresh()
        for solarEnergyStation in self.__SolarPanels:
            solarEnergyStation.refresh(self.current_time)
        self.__HydroEnergyStation.refresh()

    def __str__(self):
        neighborhood_strings = [f'Neighborhood {i + 1} - Demand={neighborhood.get_demand()}' for i, neighborhood in
                                enumerate(self.neighborhoods)]
        hospital_strings = [f'Hospital - Demand={self.hospital.get_demand()}']
        police_strings = [f'Police Department - Demand={self.policeDepartment.get_demand()}']
        fire_string = [f'Fire Department - Demand={self.fireDepartment.get_demand()}']
        total_demand = sum(neighborhood.get_demand() for neighborhood in
                           self.neighborhoods) + self.hospital.get_demand() + self.policeDepartment.get_demand() + self.fireDepartment.get_demand()

        windStation_string = [f'Wind Station {i + 1} - Generation={wind.get_generation()}' for i, wind in
                              enumerate(self.__WindTurbines)]
        solarStation_string = [f'{len(self.__SolarPanels)} solar panels - Generation={self.__solar_generation}']
        hydroStation_string = [f'Hydro Station - Generation={self.__wind_generation}']
        ffStation_string = [f'Fossil Fuel - Generation={self.__fossilFuelGeneration}']

        total_generation = self.get_green_generation() + self.__fossilFuelGeneration

        return ('\n'*1+ f'{self.city_name}:\n' +
                f'Day {self.current_time[0]}, {self.current_time[1]} during the {self.current_time[2]}\n\n' +
                '\n'.join(neighborhood_strings) + '\n' +
                '\n'.join(hospital_strings) + '\n' +
                '\n'.join(police_strings) + '\n' +
                '\n'.join(fire_string) + '\n' +
                f'\nTotal Demand = {total_demand}\n\n' +
                '\n'.join(windStation_string) + '\n' +
                '\n'.join(solarStation_string) + '\n' +
                '\n'.join(hydroStation_string) + '\n' +
                '\n'.join(ffStation_string) + '\n' +
                f'\nTotal Generation = {total_generation}\n\n' +
                f'Balance = {self.get_balance()}'+'\n')

    def get_solar_generation(self):
        return self.__solar_generation

    # TODO - }

    def __update_demand(self):
        demand = 0
        for neighborhood in self.neighborhoods:
            demand += neighborhood.get_demand()
        demand += self.hospital.get_demand()
        demand += self.policeDepartment.get_demand()
        demand += self.fireDepartment.get_demand()
        return demand

    def get_demand(self):
        return self.demand

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_hospital(self):
        return self.hospital

    def get_police_department(self):
        return self.policeDepartment

    def get_fire_department(self):
        return self.fireDepartment

    def get_ff_station(self):
        return self.FossilFuelEnergyStation

    def update_ff_generation(self):
        if self.get_balance() > 0:
            self.FossilFuelEnergyStation.decrease_generation(self.get_balance())
        else:
            self.FossilFuelEnergyStation.increase_generation(self.get_balance())
