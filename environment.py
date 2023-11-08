import time


class SmartGridEnvironment:
    def __init__(self, city):
        self.current_time = (1, "Monday", "day")
        self.city = city
        self.generation = self.get_generation()
        self.demand = self.get_demand()

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city

    def get_demand(self):
        return self.city.get_demand()

    def get_generation(self):
        return self.city.get_generation(self.current_time)

    def get_balance(self):
        return self.get_generation() - self.get_demand()

    def get_status(self):
        return self.demand, self.generation, self.get_demand() - self.get_generation()

    def get_time(self):
        return self.current_time

    def update(self):
        day, weekday, day_or_night = self.current_time
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_or_night == "day":
            self.current_time = (day, weekday, "night")
        else:
            self.current_time = (day + 1, days_of_week[(days_of_week.index(weekday) + 1) % len(days_of_week)], "day")
        self.city.get_generation(self.current_time)
