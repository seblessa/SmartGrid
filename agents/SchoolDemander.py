from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.agent import Agent
import asyncio


class SchoolDemander(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.generation = 0

    def get_generation(self):
        return self.generation

    def set_generation(self, generation):
        self.generation = generation

    async def setup(self):
        self.generation = 0
        self.add_behaviour(self.ReceivingMessages())
        self.add_behaviour(self.SendGeneration())

    class ReceivingMessages(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "neighborhood_controller@localhost":
                    self.agent.set_generation(int(message.metadata.get('generation')))
                else:
                    print(f"School Demander Agent Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending generation produced!")
            msg = Message(to="neighborhood_controller@localhost")  # Instantiate the message
            msg.set_metadata("generation", str(self.agent.get_generation()))
            msg.body = "Values sent!"

            await self.send(msg)
