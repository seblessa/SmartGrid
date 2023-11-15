import random

BASE_ENERGY = 100


class Structure:
    def __init__(self):
        self.demand = 0
        self.generation = 0
        self.online = False

    def get_demand(self):
        return self.demand

    def get_generation(self):
        return self.generation

    def update_generation(self, energy):
        self.generation += energy

    def refresh(self, energy):
        self.generation = energy
        self.online = True if self.generation - self.demand >= 0 else False


class House(Structure):
    def __init__(self, n):
        super().__init__()
        self.n_people = n
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = self.n_people * BASE_ENERGY
        return self.demand

    def get_n_people(self):
        return self.n_people


class School(Structure):
    def __init__(self, houses_in_neighborhood):
        super().__init__()
        self.houses = houses_in_neighborhood
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for house in self.houses:
            self.demand += house.get_demand()-2*BASE_ENERGY
        return self.demand


class Neighborhood:
    def __init__(self):
        houses = [House(random.randint(2, 7)) for _ in range(random.randint(8, 12))]
        self.houses = houses
        self.school = School(houses)
        self.generation = 0

    def update_generation(self, energy):
        self.generation = energy
        self.refresh()

    def get_n_houses(self):
        return len(self.houses)

    def get_houses_demand(self):
        return sum([house.get_demand() for house in self.houses])

    def get_school_demand(self):
        return self.school.get_demand()

    def get_demand(self):
        return self.get_houses_demand() + self.get_school_demand()

    def refresh(self):
        generation = self.generation
        for house in self.houses:
            min_gen = min(house.get_demand(), generation)
            generation = max(0, generation - min_gen)
            house.refresh(min_gen)
        min_gen = min(self.school.get_demand(), generation)
        self.school.refresh(min_gen)

    def __str__(self):
        house_strings = [f'House {i + 1} - Demand={house.get_demand()}' for i, house in enumerate(self.houses)]
        return '\n'.join(
            house_strings) + f'\nSchool - Demand={self.school.get_demand()}\n\nTotal = {self.get_demand()}\n\n'


class Hospital(Structure):
    def __init__(self, demand_from_neighborhoods):
        super().__init__()
        self.demand = demand_from_neighborhoods * 0.7


class PoliceDepartment(Structure):
    def __init__(self, neighborhoods):
        super().__init__()
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 2
        return self.demand


class FireDepartment(Structure):
    def __init__(self, neighborhoods):
        super().__init__()
        self.neighborhoods = neighborhoods
        self.demand = self.__update_demand()

    def __update_demand(self):
        self.demand = 0
        for neighborhood in self.neighborhoods:
            self.demand += neighborhood.get_demand() / 3
        return self.demand


class WindEnergyStation:
    def __init__(self):
        self.generation = 0
        self.conditions = [
            ("Not generating", 1), ("Not favorable", 10), ("Mildly favorable", 9),
            ("Favorable", 8), ("Very favorable", 7), ("Maximum generation", 6)
        ]
        self.current_condition_index = 1

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
            self.generation = 2500
        elif condition == "Mildly favorable":
            self.generation = 5000
        elif condition == "Favorable":
            self.generation = 7500
        elif condition == "Very favorable":
            self.generation = 10000
        elif condition == "Maximum generation":
            self.generation = 15000


class SolarEnergyStation:
    def __init__(self):
        self.generation = 100

    def get_generation(self):
        return self.generation

    def refresh(self, time):
        day, weekday, day_or_night = time
        if day_or_night == "day":
            self.generation = random.randint(1000, 1500)
        else:
            self.generation = 0


class HydroEnergyStation:
    def __init__(self):
        self.generation = 25000

    def get_generation(self):
        return self.generation

    def refresh(self):
        values = [250, 1000, 5750, 12500, 18000, 25000, 31500]
        index = random.randint(0, len(values) - 1)
        self.generation = values[index]


class FossilFuelEnergyStation:
    def __init__(self):
        self.generation = 0

    def get_generation(self):
        return self.generation

    def increase_generation(self, increase_value):
        self.generation += increase_value

    def decrease_generation(self, decrease_value):
        self.generation = max(0, self.generation - decrease_value)
