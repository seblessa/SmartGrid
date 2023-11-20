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
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.__hydro_generation = 10000

    def set_generation(self, generation):
        """
        Sets the hydro energy generation level.

        Args:
            generation (int): The hydro energy generation level.
        """
        self.__hydro_generation = generation

    async def setup(self):
        """
        Set up the HydroEnergyGenerator agent by adding a behavior for updating energy generation.
        """
        # print("Hydro Generator started")
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
                if message_author == "time_controller@localhost":
                    # print(f"HydroEnergyController Received {message.body} message from: time_controller.")
                    day, week_day, day_or_night = message.body

                    if week_day in ["Monday", "Sunday"]:
                        self.agent.set_generation(random.randint(10000, 12000))

                    elif week_day in ["Tuesday", "Saturday"]:
                        self.agent.set_generation(random.randint(12000, 14000))

                    elif week_day in ["Wednesday", "Friday"]:
                        self.agent.set_generation(random.randint(14000, 16000))

                    elif week_day == "Thursday":
                        self.agent.set_generation(random.randint(16000, 18000))

                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                    await send_behaviour.wait()
                else:
                    print(f"Hydro Energy Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending hydro energy generation information to the green power controller.
        """
        async def run(self):
            # print("Sending all Hydro generation produced!")
            msg = Message(to="green_power_controller@localhost")
            data_to_send = {"solar_generation": self.agent.__hydro_generation}
            msg.body = json.dumps(data_to_send)
            await self.send(msg)
