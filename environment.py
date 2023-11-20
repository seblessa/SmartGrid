from Structures import *
import random


class SmartGridEnvironment:
    def __init__(self, city_name="Porto"):
        self.city_name = city_name

        self.neighborhoods = [Neighborhood() for _ in range(random.randint(3, 6))]
        self.hospital = Hospital(sum([neighborhood.get_houses_demand() for neighborhood in self.neighborhoods]))
        self.policeDepartment = PoliceDepartment(self.neighborhoods)
        self.fireDepartment = FireDepartment(self.neighborhoods)

        self.__WindTurbines = [WindTurbine() for _ in range(random.randint(3, 7))]
        self.__SolarPanels = [SolarPanel() for _ in range(random.choice([16, 25, 36, 49, 64]))]
        self.__HydroEnergyStation = HydroEnergyStation()

        self.FossilFuelEnergyStation = FossilFuelEnergyStation()

    def get_city_name(self):
        return self.city_name

    def get_neighborhoods(self):
        return self.neighborhoods

    def get_hospital(self):
        return self.hospital

    def get_police_department(self):
        return self.policeDepartment

    def get_fire_department(self):
        return self.fireDepartment

    def get_name(self):
        return self.city_name

    def get_wind_turbines(self):
        return self.__WindTurbines

    def get_solar_panels(self):
        return self.__SolarPanels

    def get_solar_generation(self):
        return sum(solar.get_generation() for solar in self.__SolarPanels)

    def get_hydro_generator(self):
        return self.__HydroEnergyStation

    def get_generation(self):
        return 0

    def get_demand(self):
        return 0

    def get_balance(self):
        return self.get_generation() - self.get_demand()

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
        solarStation_string = [f'{len(self.__SolarPanels)} solar panels - Generation={sum(panel.get_generation() for panel in self.__SolarPanels)}']
        hydroStation_string = [f'Hydro Station - Generation={sum(panel.get_generation() for panel in self.__wind_generation)}']
        ffStation_string = [f'Fossil Fuel - Generation={sum(panel.get_generation() for panel in self.__fossilFuelGeneration)}']

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
