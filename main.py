from environment import SmartGridEnvironment
from agents import *
import spade


async def main():
    city = SmartGridEnvironment()

    TIMEOUT = 3

    ff = FossilFuelEnergyGenerator("fossil_fuel_power_generator@localhost", "SmartGrid", city.get_fossil_fuel_generator())
    await ff.start()

    grid = GridControllerAgent("grid_controller@localhost", "SmartGrid", city)
    await grid.start()

    neighborhood = NeighborhoodController("neighborhood_controller@localhost", "SmartGrid", city.get_neighborhoods())
    await neighborhood.start()

    hospital = DemanderAgent("hospital_demander@localhost", "SmartGrid", city.get_hospital())
    await hospital.start()

    fire = DemanderAgent("fire_station_demander@localhost", "SmartGrid", city.get_police_department())
    await fire.start()

    police = DemanderAgent("police_station_demander@localhost", "SmartGrid", city.get_fire_department())
    await police.start()

    green = GreenPowerControllerAgent("green_power_controller@localhost", "SmartGrid")
    await green.start()

    wind = WindEnergyController("wind_energy_controller@localhost", "SmartGrid", city.get_wind_turbines())
    await wind.start()

    solar = SolarEnergyController("solar_energy_controller@localhost", "SmartGrid", city.get_solar_panels())
    await solar.start()

    hydro = HydroEnergyGenerator("hydro_energy_generator@localhost", "SmartGrid", city.get_hydro_generator())
    await hydro.start()

    mapdrawer = MapDrawerAgent("map_drawer@localhost", "SmartGrid", city, TIMEOUT)
    await mapdrawer.start()

    time = TimeAgent("time_agent@localhost", "SmartGrid", city, TIMEOUT)
    await time.start()

    await spade.wait_until_finished(grid)
    await spade.wait_until_finished(green)
    await spade.wait_until_finished(solar)
    await spade.wait_until_finished(hydro)
    await spade.wait_until_finished(ff)
    await spade.wait_until_finished(neighborhood)
    await spade.wait_until_finished(hospital)
    await spade.wait_until_finished(fire)
    await spade.wait_until_finished(police)
    await spade.wait_until_finished(mapdrawer)
    await spade.wait_until_finished(time)


if __name__ == "__main__":
    spade.run(main())
