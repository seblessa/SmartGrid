import asyncio

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class WindEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("WindEnergyController started")
        b = self.SendGeneration()
        self.add_behaviour(b)

        await super().setup()

    class SendGeneration(CyclicBehaviour):
        def get_wind_generation(self):
            for wind_station in self.agent.env.get_wind_stations():
                wind_station.refresh()
            return sum([wind_station.get_generation() for wind_station in self.agent.env.get_wind_stations()])

        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="green_power_generator@localhost")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = str(self.get_wind_generation())  # Set the message content

            await self.send(msg)
            await asyncio.sleep(3)
            # print("Message sent!")


class SolarEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("SolarEnergyController started")
        b = self.SendGeneration()
        self.add_behaviour(b)

        await super().setup()

    class SendGeneration(CyclicBehaviour):
        def get_solar_generation(self):
            for solar_station in self.agent.env.get_solar_stations():
                solar_station.refresh(self.agent.env.get_time())
            return sum([solar_station.get_generation() for solar_station in self.agent.env.get_solar_stations()])

        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="green_power_generator@localhost")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = str(self.get_solar_generation())  # Set the message content

            await self.send(msg)
            await asyncio.sleep(3)
            # print("Message sent!")


class HydroEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("HydroEnergyController started")
        b = self.SendGeneration()
        self.add_behaviour(b)

        await super().setup()

    class SendGeneration(CyclicBehaviour):
        def get_hydro_generation(self):
            self.agent.env.get_hydro_station().refresh()
            return self.agent.env.get_hydro_station().get_generation()

        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="green_power_generator@localhost")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = str(self.get_hydro_generation())  # Set the message content

            await self.send(msg)
            await asyncio.sleep(3)
            # print("Message sent!")


class GreenPowerControllerAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.__wind_generation = 0
        self.__solar_generation = 0
        self.__hydro_generation = 0

    def get_wind_generation(self):
        return self.__wind_generation

    def set_wind_generation(self, wind_generation):
        self.__wind_generation = wind_generation

    def get_solar_generation(self):
        return self.__solar_generation

    def set_solar_generation(self, solar_generation):
        self.__solar_generation = solar_generation

    def get_hydro_generation(self):
        return self.__hydro_generation

    def set_hydro_generation(self, hydro_generation):
        self.__hydro_generation = hydro_generation

    async def setup(self):
        # print("GreenPowerControllerAgent started")

        wind_controller = WindEnergyController("wind_energy_generator@localhost", "SmartGrid", self.env)
        solar_controller = SolarEnergyController("solar_energy_generator@localhost", "SmartGrid", self.env)
        hydro_controller = HydroEnergyController("hydro_energy_generator@localhost", "SmartGrid", self.env)

        await asyncio.gather(
            wind_controller.start(),
            solar_controller.start(),
            hydro_controller.start()
        )

        self.add_behaviour(self.SendGeneration())
        self.add_behaviour(self.ReceivingMessages())

        # Call the setup method of the superclass
        await super().setup()

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "wind_energy_generator@localhost":
                    received_integer = int(message.body)
                    self.agent.set_wind_generation(received_integer)
                elif message_author == "solar_energy_generator@localhost":
                    received_integer = int(message.body)
                    self.agent.set_solar_generation(received_integer)
                elif message_author == "hydro_energy_generator@localhost":
                    received_integer = int(message.body)
                    self.agent.set_hydro_generation(received_integer)
                else:
                    print(f"Received '{message.body}' message from: {message_author}.")

    class SendGeneration(CyclicBehaviour):
        def get_green_generation(self):
            return int(self.agent.get_wind_generation()) + int(self.agent.get_solar_generation()) + int(
                self.agent.get_hydro_generation())

        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="grid_controller@localhost")  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = str(self.get_green_generation())  # Set the message content

            await self.send(msg)
            await asyncio.sleep(3)
            # print("Message sent!")


class GridControllerAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    async def setup(self):
        # print("GridControllerAgent started")
        b = self.ReceivingMessages()
        self.add_behaviour(b)

        await super().setup()

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "green_power_generator@localhost":
                    received_integer = int(message.body)
                    self.agent.env.set_green_generation(received_integer)
                else:
                    print(f"Received '{message.body}' message from: {message_author}.")


# TODO: CODE BELOW NOT REVISIONED


class EnergyConsumerAgent(Agent):
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


class NeighborhoodControllerAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password, env)
        self.add_behaviour(self.UpdateDemandBehav())
        self.neighborhood = env.get_neighborhoods()

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
