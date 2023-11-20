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

    def update_generation(self, energy):
        """
        Update the generation of the structure.
        :param energy: The energy to add to the generation.
        """
        self.generation += energy

    def refresh(self, energy):
        """
        Refresh the structure with new energy and update online status.
        :param energy: The new energy for the structure.
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
            house.refresh(min_gen)
        min_gen = min(self.school.get_demand(), energy)
        self.school.refresh(min_gen)

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
        self.generation = 100
        self.conditions = [
            ("Not generating", 1), ("Not favorable", 10), ("Mildly favorable", 9),
            ("Favorable", 8), ("Very favorable", 7), ("Maximum generation", 6)
        ]
        self.current_condition_index = 1

    def get_generation(self):
        """
        Get the generation of the wind turbine.
        :return: The generation of the wind turbine.
        """
        return int(self.generation)

    def refresh(self):
        """
        Refresh the wind turbine's generation based on conditions.
        """
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
            self.generation = 2500
        elif condition == "Mildly favorable":
            self.generation = 5000
        elif condition == "Favorable":
            self.generation = 7500
        elif condition == "Very favorable":
            self.generation = 10000
        elif condition == "Maximum generation":
            self.generation = 15000


class SolarPanel:
    def __init__(self):
        """
        Initialize a new solar panel with default values.
        """
        self.generation = 100

    def get_generation(self):
        """
        Get the generation of the solar panel.
        :return: The generation of the solar panel.
        """
        return int(self.generation)

    def refresh(self, time):
        """
        Refresh the solar panel's generation based on time of day.
        :param time: Tuple containing day, weekday, and day_or_night.
        """
        day, weekday, day_or_night = time
        if day_or_night == "day":
            self.generation = random.randint(1000, 1500)
        else:
            self.generation = 0


class HydroEnergyStation:
    def __init__(self):
        """
        Initialize a new hydro energy station with default values.
        """
        self.generation = 100

    def get_generation(self):
        """
        Get the generation of the hydro energy station.
        :return: The generation of the hydro energy station.
        """
        return int(self.generation)

    def refresh(self):
        """
        Refresh the hydro energy station's generation with random values.
        """
        values = [250, 1000, 2500, 5000, 7500, 1000, 12500]
        index = random.randint(0, len(values) - 1)
        self.generation = values[index]


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

    def increase_generation(self, increase_value):
        """
        Increase the generation of the fossil fuel energy station.
        :param increase_value: The value to increase the generation by.
        """
        self.generation += increase_value

    def decrease_generation(self, decrease_value):
        """
        Decrease the generation of the fossil fuel energy station.
        :param decrease_value: The value to decrease the generation by.
        """
        self.generation = max(0, self.generation - decrease_value)
