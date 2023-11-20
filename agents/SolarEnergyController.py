from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SolarEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.time = env.get_time()
        self.__solar_generation = 0

    def get_solar_generation(self):
        for panel in self.env.get_solar_panels():
            self.__solar_generation += panel.get_generation()
        return int(self.__solar_generation)

    def sum_solar_generation(self, solar_generation):
        self.__solar_generation += solar_generation

    async def setup(self):
        # print("SolarEnergyController started")
        self.__solar_generation = 0
        self.add_behaviour(self.SendGeneration())

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print(f"Sending all solar generation produced: {self.agent.get_solar_generation()}")
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("solar_generation", str(self.agent.get_solar_generation()))
            msg.body = "Sending all solar generation produced!"
            await self.send(msg)
