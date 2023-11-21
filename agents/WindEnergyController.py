import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class WindEnergyController(Agent):
    """
    Represents an agent that controls and manages multiple wind energy generators.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """
    def __init__(self, jid, password, generators):
        super().__init__(jid, password)
        self.generators = generators
        self.wind_generation = 0

    def sum_wind_generation(self, wind_generation):
        """
        Updates the total wind energy generation by adding the provided wind generation.

        Args:
            wind_generation (int): The wind energy generation to be added.
        """
        self.wind_generation += wind_generation

    async def setup(self):
        """
        Set up the WindEnergyController agent by adding behaviors for updating wind energy generation and starting wind energy generators.
        """
        self.add_behaviour(self.SendGeneration())
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        """
        A cyclic behavior for updating wind energy generation based on messages received from wind energy generators.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "time_agent@localhost":
                    # print(f"Wind Energy Generator received {message.body} message from: time_controller.")
                    # day, week_day, day_or_night = json.loads(message.body)

                    for generator in self.agent.generators:
                        generator.set_generation(random.randint(0, 3000))

                    self.agent.wind_generation = sum(generator.get_generation() for generator in self.agent.generators)

                    self.agent.add_behaviour(self.agent.SendGeneration())
                else:
                    print(f"Wind Energy Controller received '{message.body}' from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending total wind energy generation information to the green power controller.
        """
        async def run(self):
            msg = Message(to="green_power_controller@localhost")
            msg.body = str(self.agent.wind_generation)
            # print(f"Sending {msg.body} wind generation produced to {msg.to}!")
            await self.send(msg)
