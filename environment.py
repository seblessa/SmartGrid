class SmartGridEnvironment:
    def __init__(self):
        self.power_generation = 0
        self.power_demand = 0
        self.power_balance = 0

    def update_demand(self, demand):
        self.power_demand += demand
        self.update_balance()

    def update_generation(self, generation):
        self.power_generation += generation
        self.update_balance()

    def update_balance(self):
        self.power_balance = self.power_generation - self.power_demand

    def get_balance(self):
        return self.power_balance

    def get_status(self):
        return self.power_demand, self.power_generation, self.power_balance
