import asyncio
import time

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

TIMEOUT = 5


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
            await asyncio.sleep(TIMEOUT)


class WindEnergyGenerator(Agent):
    def __init__(self, jid, password, turbine):
        super().__init__(jid, password)
        self.turbine = turbine

    async def setup(self):
        # print("WindEnergyGenerator started")
        self.add_behaviour(self.SendGeneration())

    class SendGeneration(OneShotBehaviour):
        def get_wind_generation(self):
            return self.agent.turbine.get_generation()

        async def run(self):
            # print("Sending wind generation produced!")
            msg = Message(to="wind_energy_controller@localhost")
            msg.set_metadata("wind_generation", str(self.get_wind_generation()))
            msg.body = "Sending wind generation produced!"
            await self.send(msg)
            await asyncio.sleep(0)


class WindEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.__wind_generation = 0

    async def get_wind_generation(self):
        for turbine in self.env.get_wind_turbine():
            wind_generator = WindEnergyGenerator("wind_energy_generator@localhost", "SmartGrid", turbine)
            await wind_generator.start()
        return int(self.__wind_generation)

    def sum_wind_generation(self, wind_generation):
        self.__wind_generation += wind_generation

    async def setup(self):
        # print("WindEnergyController started")
        self.add_behaviour(self.ReceivingMessages())
        self.add_behaviour(self.SendGeneration())

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "wind_energy_generator@localhost":
                    self.agent.sum_wind_generation(int(message.metadata.get('wind_generation')))
                else:
                    print(f"Wind Controller Received '{message.body}' message from: {message_author}.")
            await asyncio.sleep(0)

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            wind_generation = await self.agent.get_wind_generation()
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("wind_generation", str(wind_generation))
            msg.body = "Sending all wind generation produced"
            await self.send(msg)
            await asyncio.sleep(0)


class SolarEnergyGenerator(Agent):
    def __init__(self, jid, password, panel):
        super().__init__(jid, password)
        self.panel = panel

    async def setup(self):
        # print("SolarEnergyController started")
        b = self.SendGeneration()
        self.add_behaviour(b)

    class SendGeneration(OneShotBehaviour):
        def get_solar_generation(self):
            return self.agent.panel.get_generation()

        async def run(self):
            # print("Sending solar generation produced by solar Panel")
            msg = Message(to="solar_energy_controller@localhost")
            msg.set_metadata("solar_generation", str(self.get_solar_generation()))
            # print(f"Sending solar generation produced by solar Panel: {self.get_solar_generation()} to solar controller")
            msg.body = "Sending solar generation produced!"
            await self.send(msg)
            await asyncio.sleep(0)


class SolarEnergyController(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.time = env.get_time()
        self.__solar_generation = 0

    async def get_solar_generation(self):
        for panel in self.env.get_solar_panels():
            solar_generator = SolarEnergyGenerator("solar_energy_generator@localhost", "SmartGrid", panel)
            await solar_generator.start()
        return int(self.__solar_generation)

    def sum_solar_generation(self, solar_generation):
        self.__solar_generation += solar_generation

    async def setup(self):
        # print("SolarEnergyController started")
        self.add_behaviour(self.ReceivingMessages())
        self.add_behaviour(self.SendGeneration())

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "solar_energy_generator@localhost":
                    self.agent.sum_solar_generation(int(message.metadata.get('solar_generation')))
                    # print(f"Solar Controller Received {int(message.metadata.get('solar_generation'))} message from: solar panel.")
                else:
                    print(f"Solar Controller Received '{message.body}' message from: {message_author}.")
            await asyncio.sleep(0)

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print(f"Sending all solar generation produced: {self.agent.get_solar_generation()}")
            solar_generation = await self.agent.get_solar_generation()
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("solar_generation", str(solar_generation))
            msg.body = "Sending all solar generation produced!"
            await self.send(msg)
            await asyncio.sleep(0)


class HydroEnergyGenerator(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.time = env.get_time()

    async def setup(self):
        # print("HydroEnergyGenerator started")
        b = self.SendGeneration()
        self.add_behaviour(b)

    class SendGeneration(OneShotBehaviour):
        def get_hydro_generation(self):
            return self.agent.env.get_hydro_generator().get_generation()

        async def run(self):
            # print("HydroEnergyGenerator sending hydro generation produced!")
            msg = Message(to="green_power_controller@localhost")
            msg.set_metadata("hydro_generation", str(self.get_hydro_generation()))
            msg.body = "Sending hydro generation produced!"
            await self.send(msg)
            await asyncio.sleep(0)


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
        self.add_behaviour(self.ReceivingMessages())
        self.add_behaviour(self.SendGeneration())

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "wind_energy_controller@localhost":
                    # print(f"Green Power Received {int(message.metadata.get('wind_generation'))} message from: wind_generation.")
                    self.agent.set_wind_generation(int(message.metadata.get('wind_generation')))
                elif message_author == "solar_energy_controller@localhost":
                    # print(f"Green Power Received {int(message.metadata.get('solar_generation'))} message from: solar_generation.")
                    self.agent.set_solar_generation(int(message.metadata.get('solar_generation')))
                elif message_author == "hydro_energy_generator@localhost":
                    # print(f"Green Power Received {int(message.metadata.get('hydro_generation'))} message from: hydro_generation.")
                    self.agent.set_hydro_generation(int(message.metadata.get('hydro_generation')))
                else:
                    print(f"Green Energy Agent Received '{message.body}' message from: {message_author}.")
            await asyncio.sleep(0)

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="grid_controller@localhost")  # Instantiate the message
            msg.set_metadata("wind_generation", str(self.agent.get_wind_generation()))
            msg.set_metadata("solar_generation", str(self.agent.get_solar_generation()))
            msg.set_metadata("hydro_generation", str(self.agent.get_hydro_generation()))
            msg.body = "Green generation values sent!"

            await self.send(msg)
            await asyncio.sleep(0)


class GridControllerAgent(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.add_behaviour(self.ReceivingMessages())

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
            await asyncio.sleep(0)
