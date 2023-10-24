from Structures import *
from random import randint
import pygame

# Create neighborhoods with houses
neighborhood1 = Neighborhood([House(randint(2, 7)) for _ in range(10)])
neighborhood2 = Neighborhood([House(randint(2, 7)) for _ in range(10)])

# Create schools
school1 = School(neighborhood1)
school2 = School(neighborhood2)

# Create hospitals
hospital1 = Hospital(neighborhood1)
hospital2 = Hospital(neighborhood2)

# Create emergency services
emergency_services1 = EmergencyServices([neighborhood1, neighborhood2])

# Create city
city1 = City("Vila Lessa", [neighborhood1, neighborhood2], [school1, school2], [hospital1, hospital2],
             [emergency_services1])

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
def draw_houses():
    pass


def draw_hospital():
    pass


def draw_school():
    pass


# Function to draw neighborhoods
def draw_neighborhoods():
    draw_houses()
    draw_school()
    draw_hospital()
    pass


# Function to draw emergency services
def draw_emergency_services():
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
