from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class HydroEnergyGenerator(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("HydroEnergyGenerator started")
        self.add_behaviour(self.SendGeneration())

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("HydroEnergyGenerator sending hydro generation produced!")
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("hydro_generation", str(self.agent.env.get_hydro_generator().get_generation()))
            msg.body = "Sending hydro generation produced!"
            await self.send(msg)
