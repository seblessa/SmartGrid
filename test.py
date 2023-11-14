import time
from Agents import *
from environment import SmartGridEnvironment
import spade


async def main():
    city = SmartGridEnvironment()

    neighborhoodController = NeighborhoodControllerAgent("NeighborhoodControllerAgent@localhost", "SmartGrid", city)
    await neighborhoodController.start()

    while True:
        day, weekday, day_night = city.get_time()
        print(f"Day: {day}, {weekday} during the {day_night}:\n")

        print(city)

        print("\n\n\n")
        city.update_time()
        time.sleep(2)

        await neighborhoodController.stop()


if __name__ == "__main__":
    spade.run(main())
