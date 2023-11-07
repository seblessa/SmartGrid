class SmartGridEnvironment:
    def __init__(self, city):
        self.city = city
        self.generation = self.__update_generation
        self.demand = self.__update_demand
        self.balance = self.__update_balance

    def set_city(self, city):
        self.city = city

    def __update_demand(self):
        self.demand = self.city.get_demand()

    def __update_generation(self):
        self.demand = self.city.get_generation()

    def __update_balance(self):
        self.balance = self.generation - self.demand

    def get_balance(self):
        return self.balance

    def get_demand(self):
        return self.demand

    def get_generation(self):
        return self.generation

    def get_status(self):
        return self.demand, self.generation, self.balance
