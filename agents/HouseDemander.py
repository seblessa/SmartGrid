from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.agent import Agent
import asyncio


class HouseDemander(Agent):
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env

    def use_generation(self, generation):
        demand = 0

        for neighborhood in self.env.neighborhoods:
            demand += neighborhood.get_houses_demand()

        for neighborhood in self.neighborhoods:
            min_gen = min(neighborhood.get_demand(), generation)
            green_generation = max(0, green_generation - min_gen)
            neighborhood.update_generation(min_gen)



        if balance >= 0:
            for neighborhood in self.env.neighborhoods:
                for house in neighborhood.houses:
                    house.refresh(house.get_demand())
        else:
            pass
            # pedir mais energia ao grid controller


    for neighborhood in self.neighborhoods:
        min_gen = min(neighborhood.get_demand(), green_generation)
        green_generation = max(0, green_generation - min_gen)
        neighborhood.update_generation(min_gen)


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
                    self.agent.use_generation(int(message.metadata.get('generation')))
                else:
                    print(f"School Demander Agent Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending generation produced!")
            msg = Message(to="neighborhood_controller@localhost")  # Instantiate the message
            msg.set_metadata("generation", str(self.agent.get_generation()))
            msg.body = "Values sent!"

            await self.send(msg)
