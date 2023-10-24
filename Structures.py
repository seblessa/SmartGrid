class Generator:
    def __init__(self, name):
        self.name = name
        self.max_output = max_output
        self.output = 0

    def set_output(self, x):
        if x <= self.max_output:
            self.output = x

    def get_output(self):
        return self.output

    def get_max_output(self):
        return self.max_output

class Building:
    def __init__(self, name):
        self.n_people = 0
        self.demand = 0
        self.name = name

    def update_n_people(self, x):
        if self.n_people + x >= 0:
            self.n_people += x
            self.update_demand()

    def update_demand(self):
        self.demand = self.n_people * 100

    def get_n_people(self):
        return self.n_people

    def get_demand(self):
        return self.demand

# Create hospital, houses, schools and emergency services.

class City:
    def __init__(self, name):
        self.name = name
        self.buildings = []

    def add_house(self, building):
        self.buildings.append(building)

    def get_demand(self):
        demand = 0
        for house in self.buildings:
            demand += house.get_demand()
        return demand

