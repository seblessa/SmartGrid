from environment import SmartGridEnvironment
from agents import *
import spade


async def start_agents(agents):
    """
    Start the provided list of agents asynchronously.

    Args:
        agents (list): List of Agent objects.

    Returns:
        None
    """
    for i, agent in enumerate(agents):
        print(i)
        await agent.start()


async def main():
    city = SmartGridEnvironment()

    agents = [
        GridControllerAgent("grid_controller@localhost", "SmartGrid", city),
        GreenPowerControllerAgent("green_power_controller@localhost", "SmartGrid"),
        WindEnergyController("wind_energy_controller@localhost", "SmartGrid", len(city.get_wind_turbines())),
        SolarEnergyController("solar_energy_controller@localhost", "SmartGrid", len(city.get_solar_panels())),
        SolarEnergyGenerator("solar_energy_generator@localhost", "SmartGrid"),
        HydroEnergyGenerator("hydro_energy_generator@localhost", "SmartGrid"),
        FossilFuelEnergyGenerator("fossil_fuel_power_generator@localhost", "SmartGrid"),
        NeighborhoodController("neighborhood_controller@localhost", "SmartGrid", city.get_neighborhoods()),
        DemanderAgent("hospital_demander@localhost", "SmartGrid", city.get_hospital()),
        DemanderAgent("fire_station_demander@localhost", "SmartGrid", city.get_police_department()),
        DemanderAgent("police_station_demander@localhost", "SmartGrid", city.get_fire_department()),

        ChronoCartographerAgent("time_agent@localhost", "SmartGrid", city, TIMEOUT)
    ]

    await start_agents(agents)


if __name__ == "__main__":
    spade.run(main())
