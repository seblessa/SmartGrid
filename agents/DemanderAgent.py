from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class DemanderAgent(Agent):
    def __init__(self, jid, password, consumer):
        super().__init__(jid, password)
        self.__consumer = consumer
        self.__demand = consumer.get_demand()

    async def setup(self):
        # print("DemanderAgent started")
        self.add_behaviour(self.ReceiveGeneration())
        self.add_behaviour(self.SendGeneration())

    class ReceiveGeneration(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "grid_controller@localhost":
                    # print(f"Demander Received {int(message.body)} message from: grid_controller.")
                    self.agent.__consumer.update_generation(int(message.body))

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending demand!")
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.__demand)
            await self.send(msg)
