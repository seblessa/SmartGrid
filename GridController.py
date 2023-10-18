from spade.behaviour import OneShotBehaviour
from SmartGrid import SmartGridAgent

class GridControllerAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.environment = None
        self.add_behaviour(self.LoadBalancingBehav())

    async def get_status(self):
        return self.environment.get_status()

    class LoadBalancingBehav(OneShotBehaviour):
        async def run(self):
            if self.agent.environment:
                message = await self.receive(timeout=10)  # Specify the timeout to handle non-blocking receive
                if message:
                    if "Increase power generation" in message.body:
                        self.agent.send_message("power_generator@localhost", "Increase power generation")
                    elif "Decrease power generation" in message.body:
                        self.agent.send_message("power_generator@localhost", "Decrease power generation")

                    # Handle the response properly if needed
                else:
                    print("Grid did not receive a message from Energy Consumer.")
            else:
                print("Error: Environment not set")
