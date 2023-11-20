from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class GridControllerAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("GridControllerAgent started")
        self.add_behaviour(self.ReceivingMessages())

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "green_power_controller@localhost":
                    self.agent.env.set_wind_generation(int(message.metadata.get('wind_generation')))
                    # print(f"Grid Received {int(message.metadata.get('wind_generation'))} message from: wind_generation.")
                    self.agent.env.set_solar_generation(int(message.metadata.get('solar_generation')))
                    # print(f"Grid Received {int(message.metadata.get('solar_generation'))} message from: solar_generation.")
                    self.agent.env.set_hydro_generation(int(message.metadata.get('hydro_generation')))
                    # print(f"Grid Received {int(message.metadata.get('hydro_generation'))} message from: hydro_generation.")
                else:
                    print(f"Grid Agent Received '{message.body}' message from: {message_author}.")
