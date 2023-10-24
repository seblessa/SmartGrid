from SmartGrid import SmartGridAgent
from spade.behaviour import OneShotBehaviour


class EnergyConsumerAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_behaviour(self.ConsumeEnergyBehav())

    async def update_demand(self, demand):
        current_demand = self.environment.get_demand()
        if current_demand + demand >= 0:
            self.environment.update_demand(demand)
        else:
            print("Error: Cannot reduce demand below 0.")

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
