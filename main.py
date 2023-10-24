import pygame
import asyncio
from Agents import PowerGeneratorAgent, GridControllerAgent, EnergyConsumerAgent
from environment import SmartGridEnvironment


async def main():
    # Initialize pygame
    pygame.init()

    # Constants for colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Screen dimensions
    SCREEN_WIDTH = 250
    SCREEN_HEIGHT = 150

    # Create a screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Smart Grid Simulation")

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    # Create agents and pass the environment
    grid_controller = GridControllerAgent('grid_controller@localhost', 'SmartGrid')
    power_generator = PowerGeneratorAgent('power_generator@localhost', 'SmartGrid')
    energy_consumer = EnergyConsumerAgent('energy_consumer@localhost', 'SmartGrid')


    # Create environment
    environment = SmartGridEnvironment()

    # Set environment for agents
    grid_controller.set_env(environment)
    power_generator.set_env(environment)
    energy_consumer.set_env(environment)

    def add_behaviors():
        grid_controller.add_behaviour(GridControllerAgent.LoadBalancingBehav())
        power_generator.add_behaviour(PowerGeneratorAgent.PowerGenerationBehav())
        energy_consumer.add_behaviour(EnergyConsumerAgent.ConsumeEnergyBehav())

    await grid_controller.start()
    await power_generator.start()
    await energy_consumer.start()

    demand_change = 100
    demand_down = False
    demand_up = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    demand_up = True
                elif event.key == pygame.K_DOWN:
                    demand_down = True

        if demand_up:
            await energy_consumer.update_demand(demand_change)
            demand_up = False
        elif demand_down:
            await energy_consumer.update_demand(demand_change * -1)
            demand_down = False

        await asyncio.sleep(1)

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
        add_behaviors()
    pygame.quit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
