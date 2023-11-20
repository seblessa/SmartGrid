import math
from environment import SmartGridEnvironment
import contextlib

with contextlib.redirect_stdout(None):
    import pygame
from agents import *
import random
import spade


async def start_agents(agents):
    for agent in agents:
        await agent.start()


async def main():
    city = SmartGridEnvironment()

    agents = [
        GridControllerAgent("grid_controller@localhost", "SmartGrid", city),
        GreenPowerControllerAgent("green_power_controller@localhost", "SmartGrid", city),
        WindEnergyController("wind_energy_controller@localhost", "SmartGrid", city),
        SolarEnergyController("solar_energy_controller@localhost", "SmartGrid", city),
        HydroEnergyGenerator("hydro_energy_generator@localhost", "SmartGrid", city),

        TimeAgent("time_agent@localhost", "SmartGrid", city)
    ]

    await start_agents(agents)

    # pygame.init()
    # pygame.display.set_caption(city.get_name())
    # clock = pygame.time.Clock()
    while True:
        # for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        pygame.quit()
        #        exit(0)

        # draw_city(city)
        print(city)


        # pygame.display.flip()
        # clock.tick(60)


def draw_city(city):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    # Set up the screen
    screen_size = (1600, 900)
    screen = pygame.display.set_mode(screen_size)

    current_time = city.get_time()

    screen.fill(WHITE)  # Fill the screen with white

    # Display current time at the top
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Day: {current_time[0]}, {current_time[1]} during the {current_time[2]}", True, BLACK)
    screen.blit(time_text, (500, 10))

    # Draw text box for current Balance
    x = int(screen_size[0] - 250)
    y = int(50)
    text_rect = pygame.Rect(x, y, 175, 60)
    pygame.draw.rect(screen, BLACK, text_rect, 2)  # Draw edges
    font = pygame.font.Font(None, 40)
    solar_text = font.render("Balance:", True, BLACK)
    balance_text = font.render(f"{city.get_balance()}", True, BLACK)
    screen.blit(solar_text, (x + 20, y + 5))
    screen.blit(balance_text, (x + 20, y + 33))

    def check_collision(a, b, width, height, existing_positions, r=20):
        new_rect = pygame.Rect(a - r, b - r, width + 2 * r, height + 2 * r)
        for existing_rect in existing_positions:
            if new_rect.colliderect(existing_rect):
                return True
        return False

    # Draw hospital, police departments, and fire departments randomly without colliding
    structure_positions = []  # Store positions to check collisions

    for i, structure in enumerate(
            [city.get_hospital(), city.get_police_department(), city.get_fire_department()]):
        base_radius = 35
        radius = base_radius * (i + 1)

        # Check if the initial positions have been already stored
        if not hasattr(structure, 'position'):
            angle = random.uniform(0, 2 * math.pi)
            x = screen_size[0] // 2 + int(radius * math.cos(angle)) - 35
            y = screen_size[1] // 2 + int(radius * math.sin(angle))

            # Check collision and adjust position if necessary
            while check_collision(x, y, 50, 50, structure_positions):
                radius += 10
                angle = random.uniform(0, 2 * math.pi)
                x = screen_size[0] // 2 + int(radius * math.cos(angle))
                y = screen_size[1] // 2 + int(radius * math.sin(angle))

            structure_positions.append(pygame.Rect(x, y, 50, 50))  # Store the position
            structure.position = (x, y)  # Save the initial position
        else:
            x, y = structure.position  # Retrieve the initial position

        # Draw structure
        structure_rect = pygame.Rect(x, y, 80, 50)
        pygame.draw.rect(screen, BLACK, structure_rect, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if structure.online else RED, (x + 60, y + 25), 5)

        font = pygame.font.Font(None, 15)
        demand_text = font.render(f"D: {structure.get_demand()}", True, BLACK)
        gen_text = font.render(f"G: {structure.get_generation()}", True, BLACK)
        screen.blit(demand_text, (x + 2, y + 25))
        screen.blit(gen_text, (x + 2, y + 35))

        # Add text label to the right of the squares
        name_text = font.render(f"{('Hospital', 'Police Station', 'Fire Station')[i]}", True,
                                BLACK)  # Replace with actual names
        screen.blit(name_text, (x + 4, y + 2))

    # Draw neighborhoods without colliding with existing structures
    neighborhood_positions = []  # Store positions to check collisions

    for i, neighborhood in enumerate(city.get_neighborhoods()):
        x = int(screen_size[0] / 2 + 400 * pygame.math.Vector2(1, 0).rotate(i * 360 / len(city.get_neighborhoods())).x)
        y = int(screen_size[1] / 2 + 250 * pygame.math.Vector2(1, 0).rotate(i * 360 / len(city.get_neighborhoods())).y)

        radius = 60 + neighborhood.get_n_houses() * 5

        # Check collision and adjust position if necessary
        while check_collision(x, y, 50, 50, structure_positions + neighborhood_positions):
            radius += 10
            angle = random.uniform(0, 360)
            x = int(screen_size[0] / 2 + 400 * pygame.math.Vector2(1, 0).rotate(angle).x)
            y = int(screen_size[1] / 2 + 250 * pygame.math.Vector2(1, 0).rotate(angle).y)

        neighborhood_positions.append(pygame.Rect(x, y, 50, 50))  # Store the position

        # Draw houses in the neighborhood
        num_houses = len(neighborhood.houses)
        radius = 60 + num_houses * 5  # Adjusted radius based on the number of houses
        angle_offset = random.uniform(0, 360)  # Random offset for initial placement

        # Check if the initial positions have been already stored
        if not hasattr(neighborhood, 'house_positions'):
            neighborhood.house_positions = []

            for j, house in enumerate(neighborhood.houses):
                angle = (j * (360 / num_houses) + angle_offset) % 360
                distance = radius

                house_x = int(x + distance * pygame.math.Vector2(1, 0).rotate(angle).x)
                house_y = int(y + distance * pygame.math.Vector2(1, 0).rotate(angle).y)

                neighborhood.house_positions.append((house_x, house_y))  # Save the initial position

        house_positions = neighborhood.house_positions

        # Draw houses with saved positions
        for j, (house_x, house_y) in enumerate(house_positions):
            house_rect = pygame.Rect(house_x - 25, house_y - 25, 50, 50)  # Increased size for the square
            pygame.draw.rect(screen, BLACK, house_rect, 2)  # Draw edges
            pygame.draw.circle(screen, GREEN if neighborhood.houses[j].online else RED, (house_x + 15, house_y - 3), 5)

            demand_text = font.render(f"D: {neighborhood.houses[j].get_demand()}", True, BLACK)
            gen_text = font.render(f"G: {neighborhood.houses[j].get_generation()}", True, BLACK)
            house_name_text = font.render(f"House {j + 1}", True, BLACK)
            screen.blit(house_name_text, (house_x - 20, house_y - 20))
            screen.blit(demand_text, (house_x - 22, house_y + 3))
            screen.blit(gen_text, (house_x - 22, house_y + 13))

        # Draw school in the neighborhood
        school_rect = pygame.Rect(x - 30, y - 30, 60, 60)
        pygame.draw.rect(screen, BLACK, school_rect, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if neighborhood.school.online else RED, (x + 15, y - 3), 5)

        font = pygame.font.Font(None, 15)
        demand_text = font.render(f"D: {neighborhood.school.get_demand()}", True, BLACK)
        gen_text = font.render(f"G: {neighborhood.school.get_generation()}", True, BLACK)
        school_name_text = font.render("School", True, BLACK)
        screen.blit(school_name_text, (x - 20, y - 25))
        screen.blit(demand_text, (x - 25, y + 5))
        screen.blit(gen_text, (x - 25, y + 15))

    # Draw solar panel
    solar_stations = city.get_solar_panels()
    solar_grid_size = int(len(solar_stations) ** 0.5)  # Calculate grid size for solar panels
    for i, station in enumerate(solar_stations):
        row = i // solar_grid_size
        col = i % solar_grid_size
        x = int(50 + (30 * col))
        y = int(120 + (30 * row))

        # Draw triangle for solar panel
        station_points = [(x + 5, y + 5), (x + 10, y + 15), (x, y + 15)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges

        # Draw blinking light in the middle of the triangle
        pygame.draw.circle(screen, GREEN if station.generation > 0 else RED, (x + 5, y + 12), 3)

    # Draw text box for solar panels
    x = int(screen_size[0] / 350 * solar_grid_size)
    y = int(20)

    solar_text_rect = pygame.Rect(x + 15, y + 20, solar_grid_size * 30, 40)
    pygame.draw.rect(screen, BLACK, solar_text_rect, 2)  # Draw edges
    font = pygame.font.Font(None, 20)

    solar_text = font.render("Solar Panels", True, BLACK)
    gen_text = font.render(f"Generating: {city.get_solar_generation()}", True, BLACK)
    screen.blit(solar_text, (x + 15 + (solar_grid_size * 30 - solar_text.get_width()) // 2, y + 27))
    screen.blit(gen_text, (x + 15 + (solar_grid_size * 30 - gen_text.get_width()) // 2, y + 43))

    # Draw wind stations
    for i, station in enumerate(city.get_wind_turbine()):
        x = int(screen_size[0] - 100)  # Adjusted the x-coordinate for a line
        y = int(screen_size[1] - (100 + 100 * i))

        # Draw triangle for wind station
        station_points = [(x - 30, y + 30), (x + 30, y + 30), (x, y - 30)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if station.generation > 0 else RED, (x + 1, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render(f"Wind Station {i + 1}", True, BLACK)
        gen_text = font.render(f"G: {station.get_generation()}", True, BLACK)
        screen.blit(station_name_text, (x - 33, y + 35))
        screen.blit(gen_text, (x - 20, y + 15))

    # Draw hydro station
    hydro_stations = city.get_hydro_generator()
    if hydro_stations:
        x = int(screen_size[0] - 200)
        y = int(screen_size[1] - 200)
        # Draw triangle for hydro station
        station_points = [(x - 30, y + 30), (x + 30, y + 30), (x, y - 30)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if hydro_stations.generation > 0 else RED, (x + 1, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render(f"Hydro Station", True, BLACK)
        gen_text = font.render(f"G: {hydro_stations.get_generation()}", True, BLACK)
        screen.blit(station_name_text, (x - 33, y + 35))
        screen.blit(gen_text, (x - 20, y + 15))

    # Draw fossil fuel station
    fossil_fuel_station = city.get_ff_station()
    if fossil_fuel_station:
        x = int(screen_size[0] - 200)
        y = int(screen_size[1] - 100)
        # Draw triangle for fossil fuel station
        station_points = [(x - 30, y + 30), (x + 30, y + 30), (x, y - 30)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if fossil_fuel_station.generation > 0 else RED, (x + 1, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render(f"Fossil Fuel Station", True, BLACK)
        gen_text = font.render(f"G: {fossil_fuel_station.get_generation()}", True, BLACK)
        screen.blit(station_name_text, (x - 45, y + 35))
        screen.blit(gen_text, (x - 20, y + 15))

    pygame.display.flip()


if __name__ == "__main__":
    spade.run(main())
