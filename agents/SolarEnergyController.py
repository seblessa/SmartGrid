import json
import random

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class SolarEnergyController(Agent):
    """
    Represents an agent that controls and manages multiple solar energy generators.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """

    def __init__(self, jid, password, generators):
        super().__init__(jid, password)
        self.generators = generators
        self.solar_generation = 0

    def sum_solar_generation(self, solar_generation):
        """
        Updates the total solar energy generation by adding the provided solar generation.

        Args:
            solar_generation (int): The solar energy generation to be added.
        """
        self.solar_generation += solar_generation

    async def setup(self):
        """
        Set up the SolarEnergyController agent by adding behaviors for updating solar energy generation and starting solar energy generators.
        """
        # print("WindEnergyController started")
        self.add_behaviour(self.SendGeneration())
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        """
         cyclic behavior for updating solar energy generation based on messages received from solar energy generators.
        """

        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "time_agent@localhost":
                    # print(f"SolarEnergy Generator received {message.body} from: time_controller.")
                    day, week_day, day_or_night = json.loads(message.body)

                    if day_or_night == "day":
                        for generator in self.agent.generators:
                            generator.set_generation(random.randint(1000, 3000))
                    else:  # day_or_night == "night":
                        for generator in self.agent.generators:
                            generator.set_generation(0)

                    self.agent.solar_generation = sum(generator.get_generation() for generator in self.agent.generators)

                    self.agent.add_behaviour(self.agent.SendGeneration())
                else:
                    print(f"Solar Energy Controller Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending total solar energy generation information to the green power controller.
        """

        async def run(self):
            msg = Message(to="green_power_controller@localhost")
            msg.body = str(self.agent.solar_generation)
            # print(f"Sending {msg.body} solar generation produced to {msg.to}!")
            await self.send(msg)
            self.agent.solar_generation = 0
            self.agent.n_generators_received = 0
