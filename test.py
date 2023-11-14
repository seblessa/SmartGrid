import time
from environment import SmartGridEnvironment


# Create city

city = SmartGridEnvironment()


while True:
    day, weekday, day_night = city.get_time()
    print(f"Day: {day}, {weekday} during the {day_night}:\n")

    print(city)

    print("\n\n\n")
    city.update_time()
    time.sleep(2)
