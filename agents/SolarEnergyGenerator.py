import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class SolarEnergyGenerator(Agent):
    """
    Represents an agent that generates solar energy.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.__solar_generation = 0

    def set_generation(self, generation):
        """
        Sets the solar energy generation level.

        Args:
             generation (int): The solar energy generation level.
        """
        self.__solar_generation = generation

    async def setup(self):
        """
        Set up the SolarEnergyGenerator agent by adding a behavior for updating solar energy generation.
        """
        # print("Solar Generator started")
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        """
        A cyclic behavior for updating solar energy generation based on messages received from the time controller.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "time_controller@localhost":
                    # print(f"SolarEnergyController Received {message.body} message from: time_controller.")
                    day, week_day, day_or_night = message.body

                    if day_or_night == "day":
                        self.agent.set_generation(random.randint(1000, 1500))
                    else:  # day_or_night == "night":
                        self.agent.set_generation(0)

                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                    await send_behaviour.wait()
                else:
                    print(f"Solar Energy Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending solar energy generation information to the solar energy controller.
        """
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="solar_energy_controller@localhost")
            msg.body = str(self.agent.__solar_generation)
            await self.send(msg)
