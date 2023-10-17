from SmartGrid import SmartGridAgent
from spade.behaviour import OneShotBehaviour

class PowerGeneratorAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.balance = 0
        self.environment = None
        self.add_behaviour(self.PowerGenerationBehav())

    async def increase_power_generation(self):
        if self.balance < 100:
            self.environment.update_generation(20)
            self.balance += 2
        else:
            print("Balance is at maximum. Cannot increase power generation further.")

    async def decrease_power_generation(self):
        if self.balance > 0:
            self.environment.update_generation(-20)
            self.balance -= 2
        else:
            print("Balance is at minimum. Already not producing energy.")

    class PowerGenerationBehav(OneShotBehaviour):
        async def run(self):
            if self.agent.environment:
                message = await self.receive(timeout=10)  # Specify the timeout to handle non-blocking receive

                if message:
                    if "Increase power generation" in message.body:
                        await self.agent.increase_power_generation()
                    elif "Decrease power generation" in message.body:
                        await self.agent.decrease_power_generation()
                else:
                    print("Did not receive a message from Grid Controller.")
            else:
                print("Error: Environment not set")
