class SmartGridEnvironment:
    def __init__(self, city):
        self.city = city
        self.generation = self.__update_generation()
        self.demand = self.__update_demand()

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city

    def __update_demand(self):
        return self.city.get_demand()

    def __update_generation(self):
        return self.city.get_generation()

    def get_balance(self):
        return self.get_generation() - self.get_demand()

    def get_status(self):
        return self.demand, self.generation, self.get_demand() - self.get_generation()

    def get_demand(self):
        return self.demand

    def get_generation(self):
        return self.generation


