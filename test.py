import time
from Structures import City
from environment import SmartGridEnvironment


# Create city
city1 = City("DCCity")

env = SmartGridEnvironment(city1)


while True:
    day, weekday, day_night = env.get_time()
    print(f"Day: {day}, {weekday} during the {day_night}:\n")

    print(city1)

    print("\n\n\n")
    env.update()
    time.sleep(2)
