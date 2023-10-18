class SmartGridEnvironment:
    def __init__(self):
        self.generation = 0
        self.demand = 0
        self.balance = 0

    def update_demand(self, demand):
        if demand >= 0:
            self.demand += demand
            self.update_balance()

    def update_generation(self, generation):
        self.generation += generation
        self.update_balance()

    def update_balance(self):
        self.balance = self.generation - self.demand

    def get_balance(self):
        return self.balance

    def get_demand(self):
        return self.demand

    def get_status(self):
        return self.demand, self.generation, self.balance
