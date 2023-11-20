from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class FossilFuelEnergyGenerator(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.__generation = 0
        self.__limit = 25000

    def set_generation(self, generation):
        self.__generation = generation

    async def setup(self):
        # print("Solar Generator started")
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "grid_controller@localhost":
                    # print(f"Fossil Fuel Generator Received {message.body} message from: grid_controller.")
                    energy_needed = int(message.body)
                    self.agent.set_generation(min(energy_needed, self.agent.__limit))
                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                    await send_behaviour.wait()
                else:
                    print(f"Fossil Fuel Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.__generation)
            await self.send(msg)
