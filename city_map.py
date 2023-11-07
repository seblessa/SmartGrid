import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from Agents import *
from Structures import *
from environment import SmartGridEnvironment

# Create city
city1 = City("Vila Lessa")

print(city1.get_demand())

env = SmartGridEnvironment(city1)

print(env.get_demand())

exit(0)


# Create agents and pass the environment


grid_controller = GridControllerAgent('grid_controller@localhost', 'SmartGrid')
power_generator = PowerGeneratorAgent('power_generator@localhost', 'SmartGrid')
energy_consumer = EnergyConsumerAgent('energy_consumer@localhost', 'SmartGrid')

# Create environment


# Set environment for agents
grid_controller.set_env(env)
power_generator.set_env(env)
energy_consumer.set_env(env)

# Constants for colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# City data
window_width = 800
window_height = 600

# Create the Pygame window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(city1.name)


# Function to draw houses
def draw_houses(env):
    pass


def draw_hospital(env):
    pass


def draw_school(env):
    pass


# Function to draw neighborhoods
def draw_neighborhoods(env):
    draw_houses(env)
    draw_school(env)
    draw_hospital(env)
    pass


# Function to draw emergency services
def draw_emergency_services(env):
    pass


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
