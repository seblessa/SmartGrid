from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class WindEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.__wind_generation = 0

    def get_wind_generation(self):
        for turbine in self.env.get_wind_turbine():
            self.__wind_generation += turbine.get_generation()
        return int(self.__wind_generation)

    def sum_wind_generation(self, wind_generation):
        self.__wind_generation += wind_generation

    async def setup(self):
        # print("WindEnergyController started")
        self.__wind_generation = 0
        self.add_behaviour(self.SendGeneration())

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("wind_generation", str(self.agent.get_wind_generation()))
            msg.body = "Sending all wind generation produced"
            await self.send(msg)
