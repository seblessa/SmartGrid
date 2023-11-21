import random

BASE_ENERGY = 100


class Structure:
    """
    This class represents a structure in the city.
    """
    def __init__(self):
        """
        Initialize a new structure with default values.
        """
        self.demand = 0
        self.generation = 0
        self.online = False

    def get_demand(self):
        """
        Get the demand of the structure.
        :return: The demand of the structure.
        """
        return int(self.demand)

    def get_generation(self):
        """
        Get the generation of the structure.
        :return: The generation of the structure.
        """
        return int(self.generation)

    def set_generation(self, energy):
        """
        Set the generation of the structure.
        :param energy: The energy to add to the generation.
        """
        self.generation = energy
        self.online = self.generation - self.demand >= 0


class House(Structure):
    def __init__(self, n):
        """
        Initialize a new house with the given number of people.
        :param n: The number of people in the house.
        """
        super().__init__()
        self.n_people = n
        self.demand = self.__update_demand()

    def __update_demand(self):
        """
        Update the demand of the house based on the number of people.
        :return: The updated demand of the house.
        """
        self.demand = self.n_people * BASE_ENERGY
        return self.demand

    def get_n_people(self):
        """
        Get the number of people in the house.
        :return: The number of people in the house.
        """
        return self.n_people


class School(Structure):
    def __init__(self, houses_in_neighborhood):
        """
        Initialize a new school with the given houses in the neighborhood.
        :param houses_in_neighborhood: List of houses in the neighborhood.
        """
        super().__init__()
        self.houses = houses_in_neighborhood
        self.demand = self.__update_demand()

    def __update_demand(self):
        """
        Update the demand of the school based on the houses in the neighborhood.
        :return: The updated demand of the school.
        """
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand() - 2 * BASE_ENERGY
        return self.demand


class Neighborhood:
    def __init__(self):
        """
        Initialize a new neighborhood with random houses and a school.
        """
        houses = [House(random.randint(2, 7)) for _ in range(random.randint(5, 11))]
        self.houses = houses
        self.school = School(houses)
        self.generation = 0

    def update_generation(self, energy):
        """
        Update the generation of the neighborhood and distribute energy to houses and school.
        :param energy: The total energy for the neighborhood.
        """
        self.generation = energy
        for house in self.houses:
            min_gen = min(house.get_demand(), energy)
            energy = max(0, energy - min_gen)
            house.set_generation(min_gen)
        min_gen = min(self.school.get_demand(), energy)
        self.school.set_generation(min_gen)

    def get_n_houses(self):
        """
        Get the number of houses in the neighborhood.
        :return: The number of houses in the neighborhood.
        """
        return len(self.houses)

    def get_houses_demand(self):
        """
        Get the total demand of all houses in the neighborhood.
        :return: The total demand of all houses in the neighborhood.
        """
        return sum([house.get_demand() for house in self.houses])

    def get_school_demand(self):
        """
        Get the demand of the school in the neighborhood.
        :return: The demand of the school in the neighborhood.
        """
        return self.school.get_demand()

    def get_demand(self):
        """
        Get the total energy demand of the neighborhood.
        :return: The total energy demand of the neighborhood.
        """
        return self.get_houses_demand() + self.get_school_demand()

    def __str__(self):
        """
        Get a string representation of the neighborhood, including each house and the school.
        :return: A string representation of the neighborhood.
        """
        house_strings = [f'House {i + 1} - Demand={house.get_demand()}' for i, house in enumerate(self.houses)]
        return '\n'.join(
            house_strings) + f'\nSchool - Demand={self.school.get_demand()}\n\nTotal = {self.get_demand()}\n\n'


class Hospital(Structure):
    def __init__(self, demand_from_neighborhoods):
        """
        Initialize a new hospital with demand from neighborhoods.
        :param demand_from_neighborhoods: The demand from neighborhoods for the hospital.
        """
        super().__init__()
        self.demand = demand_from_neighborhoods * 0.7


class PoliceDepartment(Structure):
    def __init__(self, neighborhoods):
        """
        Initialize a new police department with demand based on neighborhoods.
        :param neighborhoods: List of neighborhoods.
        """
        super().__init__()
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        """
        Update the demand of the police department based on neighborhoods.
        :return: The updated demand of the police department.
        """
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 2
        return self.demand


class FireDepartment(Structure):
    def __init__(self, neighborhoods):
        """
        Initialize a new fire department with demand based on neighborhoods.
        :param neighborhoods: List of neighborhoods.
        """
        super().__init__()
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        """
        Update the demand of the fire department based on neighborhoods.
        :return: The updated demand of the fire department.
        """
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 3
        return self.demand


class WindTurbine:
    def __init__(self):
        """
        Initialize a new wind turbine with default values.
        """
        self.generation = 0

    def set_generation(self, generation):
        """
        Set the generation of the wind turbine.
        :param generation: The generation of the wind turbine.
        """
        self.generation = generation

    def get_generation(self):
        """
        Get the generation of the wind turbine.
        :return: The generation of the wind turbine.
        """
        return int(self.generation)



class SolarPanel:
    def __init__(self):
        """
        Initialize a new solar panel with default values.
        """
        self.generation = 0

    def set_generation(self, generation):
        """
        Set the generation of the wind turbine.
        :param generation: The generation of the wind turbine.
        """
        self.generation = generation

    def get_generation(self):
        """
        Get the generation of the solar panel.
        :return: The generation of the solar panel.
        """
        return int(self.generation)


class HydroEnergyStation:
    def __init__(self):
        """
        Initialize a new hydro energy station with default values.
        """
        self.generation = 0

    def get_generation(self):
        """
        Get the generation of the hydro energy station.
        :return: The generation of the hydro energy station.
        """
        return int(self.generation)

    def set_generation(self, generation):
        """
        Set the generation of the hydro energy station.
        :param generation: The generation of the hydro energy station.
        """
        self.generation = generation


class FossilFuelEnergyStation:
    def __init__(self):
        """
        Initialize a new fossil fuel energy station with default values.
        """
        self.generation = 0

    def get_generation(self):
        """
        Get the generation of the fossil fuel energy station.
        :return: The generation of the fossil fuel energy station.
        """
        return int(self.generation)

    def set_generation(self, generation):
        """
        Set the generation of the fossil fuel energy station.
        :param generation: The generation of the fossil fuel energy station.
        """
        self.generation = generation
