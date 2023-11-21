import json
import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class HydroEnergyGenerator(Agent):
    """
    Represents an agent that generates hydro energy.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """

    def __init__(self, jid, password, generator):
        super().__init__(jid, password)
        self.generator = generator
        self.hydro_generation = 0

    async def setup(self):
        """
        Set up the HydroEnergyGenerator agent by adding a behavior for updating energy generation.
        """
        # print("Hydro Generator started")
        self.add_behaviour(self.SendGeneration())
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        """
        A cyclic behavior for updating hydro energy generation based on the time of the day and week.
        """

        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "time_agent@localhost":
                    # print(f"HydroEnergyController Received {message.body} message from: time_controller.")
                    day, week_day, day_or_night = json.loads(message.body)

                    if week_day in ["Monday", "Sunday"]:
                        self.agent.generator.set_generation(random.randint(100000, 130000))

                    elif week_day in ["Tuesday", "Saturday"]:
                        self.agent.generator.set_generation(random.randint(130000, 160000))

                    elif week_day in ["Wednesday", "Friday"]:
                        self.agent.generator.set_generation(random.randint(160000, 190000))

                    elif week_day == "Thursday":
                        self.agent.generator.set_generation(random.randint(190000, 210000))

                    self.agent.hydro_generation = self.agent.generator.get_generation()

                    self.agent.add_behaviour(self.agent.SendGeneration())
                else:
                    print(f"Hydro Energy Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending hydro energy generation information to the green power controller.
        """

        async def run(self):
            msg = Message(to="green_power_controller@localhost")
            msg.body = str(self.agent.hydro_generation)
            # print(f"Sending {msg.body} Hydro generation produced to {msg.to}!")
            await self.send(msg)
