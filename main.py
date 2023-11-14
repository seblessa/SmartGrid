import contextlib
import pygame
import random
from Agents import *
from Structures import *
from environment import SmartGridEnvironment

# Cria a cidade
city = SmartGridEnvironment("Porto")

# Cria os agentes e passa o ambiente
grid_controller = GridControllerAgent('grid_controller@localhost', 'SmartGrid', city)
power_generator = PowerGeneratorAgent('power_generator@localhost', 'SmartGrid', city)
energy_consumer = EnergyConsumerAgent('energy_consumer@localhost', 'SmartGrid', city)

# Constantes para cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Inicializa o Pygame
pygame.init()

# Dados da cidade
window_width = 2000
window_height = 1400

# Número total de áreas na tela
num_areas = 6

# Calcula o tamanho de cada célula
cell_width = window_width // 3
cell_height = window_height // 2

# Associa a cada área um valor de 1 a 6
area_values = list(range(1, num_areas + 1))

# Mapeia a área de cada valor
area_mapping = {
    1: (0, 0, cell_width, cell_height),
    2: (cell_width, 0, cell_width, cell_height),
    3: (2 * cell_width, 0, cell_width, cell_height),
    4: (0, cell_height, cell_width, cell_height),
    5: (cell_width, cell_height, cell_width, cell_height),
    6: (2 * cell_width, cell_height, cell_width, cell_height)
}

# Cria a janela do Pygame
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(city.get_city_name())


# Função para desenhar casas com separação
def draw_houses(neighborhood, area_rect):
    n_houses = neighborhood.get_n_houses()
    spacing = 150  # Ajusta o espaçamento entre as casas
    house_x = area_rect[0] + 50  # Coordenada x inicial
    house_y = area_rect[1] + 50  # Coordenada y inicial
    for _ in range(n_houses):
        draw_single_house(house_x, house_y)
        house_x += spacing  # Move para a próxima casa


def draw_single_house(x, y):
    house_color = RED
    house_width = 60
    house_height = 60
    pygame.draw.rect(window, house_color, (x, y, house_width, house_height))


def draw_hospital(x, y):
    hospital_color = (255, 255, 255)
    hospital_border_color = (0, 0, 0)
    hospital_width = 120
    hospital_height = 120
    pygame.draw.rect(window, hospital_color, (x, y, hospital_width, hospital_height))
    pygame.draw.rect(window, hospital_border_color, (x, y, hospital_width, hospital_height), 2)
    pygame.draw.line(window, (255, 0, 0), (x, y + hospital_height // 2), (x + hospital_width, y + hospital_height // 2),
                     2)
    pygame.draw.line(window, (255, 0, 0), (x + hospital_width // 2, y), (x + hospital_width // 2, y + hospital_height),
                     2)


def draw_school(x, y):
    school_color = GREEN
    school_width = 120
    school_height = 120
    pygame.draw.rect(window, school_color, (x, y, school_width, school_height))


def draw_police_station(x, y):
    police_color = (255, 255, 255)
    police_border_color = (0, 0, 0)
    police_width = 120
    police_height = 120
    pygame.draw.rect(window, police_color, (x, y, police_width, police_height))
    pygame.draw.rect(window, police_border_color, (x, y, police_width, police_height), 2)
    pygame.draw.circle(window, (255, 255, 0), (x + police_width // 2, y + police_height // 2), police_width // 2, 2)


def draw_fire_station(x, y):
    fire_color = (255, 255, 255)
    fire_border_color = (0, 0, 0)
    fire_width = 120
    fire_height = 120
    pygame.draw.rect(window, fire_color, (x, y, fire_width, fire_height))
    pygame.draw.rect(window, fire_border_color, (x, y, fire_width, fire_height), 2)
    pygame.draw.circle(window, (255, 0, 0), (x + fire_width // 2, y + fire_height // 2), fire_width // 2, 2)


def draw_city(city):
    for area_number, neighborhood in enumerate(city.get_neighborhoods()):
        draw_houses(neighborhood, area_mapping[area_number])

        # Corrected indices for accessing coordinates
        draw_school(area_mapping[area_number][0], area_mapping[area_number][1])

        if area_number == 3 or area_number == 6:
            draw_fire_station(area_mapping[area_number][0], area_mapping[area_number][1])

        if area_number == 2 or area_number == 4 or area_number == 6:
            draw_police_station(area_mapping[area_number][0], area_mapping[area_number][1])
            draw_hospital(area_mapping[area_number][0], area_mapping[area_number][1])


# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpa a tela
    window.fill((255, 255, 255))  # Preenche a janela com a cor branca

    # Chama a função para desenhar bairros (neste exemplo, serão selecionadas 3 áreas aleatórias)
    draw_city(city)

    # Atualiza o display
    pygame.display.flip()

# Sai do Pygame
pygame.quit()
