import pygame
import random

# Inicialize o pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Smart Grid Simulation")

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Defina o número de nós e seus estados iniciais (ligado/desligado)
num_nodes = 5
node_states = [random.choice([True, False]) for _ in range(num_nodes)]

# Relógio para controle de atualização de tela
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpe a tela
    screen.fill(WHITE)

    # Atualize a representação gráfica da smart grid
    node_x = 100
    for state in node_states:
        if state:
            pygame.draw.circle(screen, GREEN, (node_x, screen_height // 2), 30)
        else:
            pygame.draw.circle(screen, RED, (node_x, screen_height // 2), 30)
        node_x += 150

    # Atualize a tela
    pygame.display.flip()

    # Atualize os estados dos nós (simulação de piscar)
    node_states = [random.choice([True, False]) for _ in range(num_nodes)]

    # Limitar a taxa de quadros por segundo
    clock.tick(2)  # 2 quadros por segundo neste exemplo

pygame.quit()
