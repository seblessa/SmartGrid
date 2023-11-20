import json
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

from agents import WindEnergyGenerator


class WindEnergyController(Agent):
    def __init__(self, jid, password, n_generators):
        super().__init__(jid, password)
        self.__n_generators = n_generators
        self.__n_generators_received = 0
        self.__wind_generation = 0

    def sum_wind_generation(self, wind_generation):
        self.__wind_generation += wind_generation

    async def setup(self):
        # print("WindEnergyController started")
        self.add_behaviour(self.UpdateGeneration())
        for i in range(self.__n_generators):
            print(i)
            agent = WindEnergyGenerator("wind_energy_generator@localhost", "SmartGrid")
            await agent.start()
        print("***")

    class UpdateGeneration(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "wind_energy_generator@localhost":
                    if self.agent.__n_generators_received == 0:
                        self.agent.__wind_generation = 0
                    # print(f"WindEnergyController Received {int(message.body)} message from: wind_generator.")
                    self.agent.__n_generators_received += 1
                    self.agent.sum_wind_generation(int(message.body))

                    if self.agent.__n_generators_received == self.agent.__n_generators:
                        send_behaviour = self.agent.SendGeneration()
                        self.agent.add_behaviour(send_behaviour)
                        await send_behaviour.wait()

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="green_power_controller@localhost")
            data_to_send = {"wind_generation": self.agent.__wind_generation}
            msg.body = json.dumps(data_to_send)
            await self.send(msg)
            self.agent.__wind_generation = 0
            self.agent.__n_generators_received = 0
