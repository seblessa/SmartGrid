from environment import SmartGridEnvironment
from Agents import *
import pygame
import random
import spade


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen_size = (1600, 900)
screen = pygame.display.set_mode(screen_size)


async def main():
    city = SmartGridEnvironment()

    # neighborhoodController = NeighborhoodControllerAgent("NeighborhoodControllerAgent@localhost", "SmartGrid", city)
    # await neighborhoodController.start()

    pygame.init()
    pygame.display.set_caption(city.get_name())
    clock = pygame.time.Clock()
    while True:
        # print(city)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        draw_city(city)
        city.update_time()
        pygame.time.delay(2000)
        pygame.display.flip()
        clock.tick(60)

        # await neighborhoodController.stop()


def draw_city(city):
    current_time = city.get_time()

    screen.fill(WHITE)  # Fill the screen with white

    # Display current time at the top
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Day: {current_time[0]}, {current_time[1]} during the {current_time[2]}", True, BLACK)
    screen.blit(time_text, (500, 10))

    # Draw hospitals, police departments, and fire departments in lines
    for i, structure_list in enumerate(
            [city.get_hospitals(), city.get_police_department(), city.get_fire_department()]):
        x = int(screen_size[0] / 2 - 110)
        y = int(screen_size[1] / 2 - 75 + i * 60)  # Adjusted y-coordinate for lines

        for j, structure in enumerate(structure_list):
            structure_rect = pygame.Rect(x + j * 100, y, 50, 50)  # Adjusted x-coordinate for lines
            pygame.draw.rect(screen, BLACK, structure_rect, 2)  # Draw edges
            pygame.draw.circle(screen, GREEN if structure.online else RED, (x + 25 + j * 100, y + 25), 5)

            font = pygame.font.Font(None, 15)
            demand_text = font.render(f"D: {structure.get_demand()}", True, BLACK)
            gen_text = font.render(f"G: {structure.get_generation()}", True, BLACK)
            screen.blit(demand_text, (x + j * 100, y + 50))
            screen.blit(gen_text, (x + j * 100, y + 60))

            # Add text label to the right of the squares
            name_text = font.render(f"{('Hospital', 'Police', 'Fire')[i]}", True, BLACK)  # Replace with actual names
            screen.blit(name_text, (x + 50 + j * 100, y + 25))

    # Draw neighborhoods
    for i, neighborhood in enumerate(city.get_neighborhoods()):
        x = int(screen_size[0] / 2 + 400 * pygame.math.Vector2(1, 0).rotate(i * 360 / len(city.get_neighborhoods())).x)
        y = int(screen_size[1] / 2 + 300 * pygame.math.Vector2(1, 0).rotate(i * 360 / len(city.get_neighborhoods())).y)

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
            pygame.draw.circle(screen, GREEN if neighborhood.houses[j].online else RED, (house_x, house_y), 5)

            demand_text = font.render(f"D: {neighborhood.houses[j].get_demand()}", True, BLACK)
            gen_text = font.render(f"G: {neighborhood.houses[j].get_generation()}", True, BLACK)
            screen.blit(demand_text, (house_x - 25, house_y - 25))
            screen.blit(gen_text, (house_x - 25, house_y - 15))

        # Draw school in the neighborhood
        school_rect = pygame.Rect(x - 30, y - 30, 60, 60)
        pygame.draw.rect(screen, BLACK, school_rect, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if neighborhood.school.online else RED, (x, y), 5)

        font = pygame.font.Font(None, 15)
        demand_text = font.render(f"D: {neighborhood.school.get_demand()}", True, BLACK)
        gen_text = font.render(f"G: {neighborhood.school.get_generation()}", True, BLACK)
        school_name_text = font.render("School", True, BLACK)
        screen.blit(school_name_text, (x - 30, y + 30))
        screen.blit(demand_text, (x - 30, y - 30))
        screen.blit(gen_text, (x - 30, y - 20))

    # Draw energy generation stations as triangles in a grid in the top left corner
    solar_stations = city.get_solar_stations()
    solar_grid_size = int(len(solar_stations) ** 0.5)  # Calculate grid size for solar panels
    for i, station in enumerate(solar_stations):
        row = i // solar_grid_size
        col = i % solar_grid_size
        x = int(screen_size[0] / 50 + (30 * col))
        y = int(screen_size[1] / 40 + (30 * row))

        # Draw triangle for solar panel
        station_points = [(x + 5, y + 5), (x + 10, y + 15), (x, y + 15)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges

        # Draw blinking light in the middle of the triangle
        pygame.draw.circle(screen, GREEN if station.generation > 0 else RED, (x + 5, y + 12), 3)

    # Draw text box for solar panels
    x = int(screen_size[0] / 350 * solar_grid_size)
    y = int(screen_size[1] / 4)
    solar_text_rect = pygame.Rect(x + 15, y, 150, 40)
    pygame.draw.rect(screen, BLACK, solar_text_rect, 2)  # Draw edges
    font = pygame.font.Font(None, 20)
    solar_text = font.render("Solar Panels:", True, BLACK)
    gen_text = font.render(f"Generating {city.get_solar_generation()}", True, BLACK)
    screen.blit(solar_text, (x + 20, y + 5))
    screen.blit(gen_text, (x + 20, y + 25))

    for i, station in enumerate(city.get_wind_stations()):
        x = int(screen_size[0] / 1.2 + 150 * i)  # Adjusted the x-coordinate for a line
        y = int(screen_size[1] / 10)

        # Draw triangle for wind station
        station_points = [(x - 15, y + 15), (x + 15, y + 15), (x, y - 15)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if station.generation > 0 else RED, (x, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render("Wind Station", True, BLACK)
        screen.blit(station_name_text, (x - 25, y + 20))

    # Draw hydro station as a triangle in the line to the right of wind stations
    hydro_stations = city.get_hydro_station()
    if hydro_stations:
        x = int(screen_size[0] / 1.2 + 150)
        y = int((screen_size[1] / 10) + 100)
        # Draw triangle for hydro station
        station_points = [(x - 15, y + 15), (x + 15, y + 15), (x, y - 15)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if hydro_stations.generation > 0 else RED, (x, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render("Hydro Station", True, BLACK)
        screen.blit(station_name_text, (x - 25, y + 20))

    # Draw fossil fuel station as a triangle in the line to the right of hydro station
    fossil_fuel_stations = city.get_ff_station()
    if fossil_fuel_stations:
        x = int(screen_size[0] / 1.2 + 150)
        y = int((screen_size[1] / 10) + 200)
        # Draw triangle for fossil fuel station
        station_points = [(x - 15, y + 15), (x + 15, y + 15), (x, y - 15)]
        pygame.draw.polygon(screen, BLACK, station_points, 2)  # Draw edges
        pygame.draw.circle(screen, GREEN if fossil_fuel_stations.generation > 0 else RED, (x, y - 15), 5)

        font = pygame.font.Font(None, 15)
        station_name_text = font.render("Fossil Fuel Station", True, BLACK)
        screen.blit(station_name_text, (x - 25, y + 20))

    pygame.display.flip()


if __name__ == "__main__":
    spade.run(main())
