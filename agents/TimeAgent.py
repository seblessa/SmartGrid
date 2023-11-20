from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class TimeAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("TimeControllerAgent started")
        self.add_behaviour(self.TimeUpdate())

    class TimeUpdate(OneShotBehaviour):
        async def run(self):
            self.agent.env.update_time()
            self.agent.env.update_generation()
            # await asyncio.sleep(TIMEOUT)
