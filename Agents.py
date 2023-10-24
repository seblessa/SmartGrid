from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SmartGridAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.environment = None

    def set_env(self, env):
        self.environment = env

    def send_message(self, receiver, message):
        class SendMessageBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=receiver)
                msg.body = message
                await self.send(msg)

        self.add_behaviour(SendMessageBehaviour())

    def receive_message(self, timeout=10):
        class ReceiveMessageBehaviour(OneShotBehaviour):
            async def run(self):
                msg = await self.receive(timeout=timeout)
                if msg:
                    print(f"Received message: {msg.body}")
                else:
                    print(f"Did not receive any message after {timeout} seconds")

        self.add_behaviour(ReceiveMessageBehaviour())


class GridControllerAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
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


class PowerGeneratorAgent(SmartGridAgent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.balance = 0
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
                    print("Power did not receive a message from Grid Controller.")
            else:
                print("Error: Environment not set")
