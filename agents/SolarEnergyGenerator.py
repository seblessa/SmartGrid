import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class SolarEnergyGenerator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.__solar_generation = 0

    def set_generation(self, generation):
        self.__solar_generation = generation

    async def setup(self):
        # print("Solar Generator started")
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
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
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="solar_energy_controller@localhost")
            msg.body = str(self.agent.__solar_generation)
            await self.send(msg)
