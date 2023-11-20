import json
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from agents import SolarEnergyGenerator


class SolarEnergyController(Agent):
    def __init__(self, jid, password, n_generators):
        super().__init__(jid, password)
        self.__n_generators = n_generators
        self.__n_generators_received = 0
        self.__solar_generation = 0

    def sum_solar_generation(self, solar_generation):
        self.__solar_generation += solar_generation

    async def setup(self):
        # print("WindEnergyController started")
        self.add_behaviour(self.UpdateGeneration())
        for i in range(self.__n_generators):
            agent = SolarEnergyGenerator("solar_energy_generator@localhost", "SmartGrid")
            await agent.start()

    class UpdateGeneration(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "solar_energy_generator@localhost":
                    if self.agent.__n_generators_received == 0:
                        self.agent.__solar_generation = 0
                    # print(f"WindEnergyController Received {int(message.body)} message from: wind_generator.")
                    self.agent.__n_generators_received += 1
                    self.agent.sum_solar_generation(int(message.body))

                    if self.agent.__n_generators_received == self.agent.__n_generators:
                        send_behaviour = self.agent.SendGeneration()
                        self.agent.add_behaviour(send_behaviour)
                        await send_behaviour.wait()

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="green_power_controller@localhost")
            data_to_send = {"solar_generation": self.agent.__solar_generation}
            msg.body = json.dumps(data_to_send)
            await self.send(msg)
            self.agent.__wind_generation = 0
            self.agent.__n_generators_received = 0
