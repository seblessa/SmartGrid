from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


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

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending green generation produced!")
            msg = Message(to="grid_controller@localhost")  # Instantiate the message
            msg.set_metadata("wind_generation", str(self.agent.get_wind_generation()))
            msg.set_metadata("solar_generation", str(self.agent.get_solar_generation()))
            msg.set_metadata("hydro_generation", str(self.agent.get_hydro_generation()))
            msg.body = "Green generation values sent!"

            await self.send(msg)
