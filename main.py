import pygame
import asyncio
from PowerGenerator import PowerGeneratorAgent
from GridController import GridControllerAgent
from EnergyConsumer import EnergyConsumerAgent
from environment import SmartGridEnvironment

# Initialize pygame
pygame.init()

# Constants for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smart Grid Simulation")

# Font for displaying text
font = pygame.font.Font(None, 36)

# Constants for adjusting demand
DEMAND_CHANGE = 100

# Initialize demand and environment
demand = 0
environment = SmartGridEnvironment()

async def main():
    global demand
    # Create agents and pass the environment
    grid_controller = GridControllerAgent('grid_controller@localhost', 'SmartGrid')
    power_generator = PowerGeneratorAgent('power_generator@localhost', 'SmartGrid')
    energy_consumer = EnergyConsumerAgent('energy_consumer@localhost', 'SmartGrid')

    grid_controller.environment = environment
    power_generator.environment = environment
    energy_consumer.environment = environment

    # Start agents and add behaviors
    await asyncio.gather(
        grid_controller.start(),
        power_generator.start(),
        energy_consumer.start()
    )

    # Main loop
    running = True
    while running:
        await asyncio.sleep(1)
        demand_down = False
        demand_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    demand_up = True
                elif event.key == pygame.K_DOWN:
                    demand_down = True

        if demand_up:
            await energy_consumer.update_demand(DEMAND_CHANGE)
        elif demand_down:
            await energy_consumer.update_demand(-DEMAND_CHANGE)

        # Clear the screen
        screen.fill(BLACK)

        demand, generation, balance = await grid_controller.get_status()

        # Display the balance, generation, and demand
        balance_text = font.render(f"Balance: {balance} KJ", True, WHITE)
        generation_text = font.render(f"Generation: {generation} KJ", True, WHITE)
        demand_text = font.render(f"Demand: {demand} KJ", True, WHITE)

        screen.blit(balance_text, (10, 10))
        screen.blit(generation_text, (10, 50))
        screen.blit(demand_text, (10, 90))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
