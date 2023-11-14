from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class SmartGridAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.environment = env

    def get_env(self):
        return self.environment

    def send_message(self, receiver, message):
        class SendMessageBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=receiver)
                msg.body = message
                await self.send(msg)

        self.add_behaviour(SendMessageBehaviour())

    def receive_message(self):
        class ReceiveMessageBehaviour(CyclicBehaviour):
            async def run(self):
                msg = await self.receive()
                print(f"Received message: {msg.body}")

        self.add_behaviour(ReceiveMessageBehaviour())


# TODO: CODE BELOW NOT REVISED


class GridControllerAgent(SmartGridAgent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password, environment)
        self.add_behaviour(self.LoadBalancingBehav())

    async def get_status(self):
        return self.environment.get_status()

    class LoadBalancingBehav(CyclicBehaviour):
        async def run(self):
            if self.agent.environment:
                message = await self.receive()
                if message:
                    if "Increase Fossil Fuel power generation" in message.body:
                        self.agent.send_message("power_generator@localhost", "Increase power generation")
                    elif "Decrease Fossil Fuel power generation" in message.body:
                        self.agent.send_message("power_generator@localhost", "Decrease power generation")

                    # Handle the response properly if needed
                else:
                    print("Grid did not receive a message from Energy Consumer.")
            else:
                print("Error: Environment not set")


class EnergyConsumerAgent(SmartGridAgent):
    def __init__(self, jid, password, environment):
        super().__init__(jid, password, environment)
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
    def __init__(self, jid, password, environment):
        super().__init__(jid, password, environment)
        self.balance = 0
        self.add_behaviour(self.PowerGenerationBehav())

    async def increase_power_generation(self):
        if self.balance < 100:
            self.environment.__update_generation(20)
            self.balance += 2
        else:
            print("Balance is at maximum. Cannot increase power generation further.")

    async def decrease_power_generation(self):
        if self.balance > 0:
            self.environment.__update_generation(-20)
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


class NeighborhoodControllerAgent(SmartGridAgent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password, env)
        self.add_behaviour(self.UpdateDemandBehav())
        self.houses = env.get_houses()
        self.school = env.get_school()
        self.hospital = env.get_hospital()

    async def update_demand(self, demand):
        current_demand = self.environment.get_demand()
        if current_demand + demand >= 0:
            self.environment.update_demand(demand)
        else:
            print("Error: Cannot reduce demand below 0.")

    class UpdateDemandBehav(OneShotBehaviour):
        async def run(self):
            if self.agent.environment:
                message = await self.receive(timeout=60)  # Specify the timeout to handle non-blocking receive
                if message:
                    if "Increase demand" in message.body:
                        await self.agent.update_demand(20)
                    elif "Decrease demand" in message.body:
                        await self.agent.update_demand(-20)

                    # Handle the response properly if needed
                else:
                    print("Neighborhood did not receive a message from Energy Consumer.")
            else:
                print("Error: Environment not set")
