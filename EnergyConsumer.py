from SmartGrid import SmartGridAgent
from spade.behaviour import OneShotBehaviour

class EnergyConsumerAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.environment = None
        # Add the behavior to the agent
        self.add_behaviour(self.ConsumeEnergyBehav())

    async def update_demand(self, demand):
        if self.environment:
            self.environment.update_demand(demand)
            await self.ConsumeEnergyBehav().on_start()
        else:
            print("Error: Environment not set")

    class ConsumeEnergyBehav(OneShotBehaviour):
        async def run(self):
            if self.agent.environment:
                balance = self.agent.environment.get_balance()

                if balance < 0:
                    self.agent.send_message("grid_controller@localhost", "Increase power generation")
                elif balance > 0:
                    self.agent.send_message("grid_controller@localhost", "Decrease power generation")

                # Handle the response properly if needed
            else:
                print("Error: Environment not set")
