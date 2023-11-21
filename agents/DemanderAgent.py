from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class DemanderAgent(Agent):
    """
    Represents an agent that demands energy from the grid controller.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
        consumer: The consumer entity associated with the agent.
    """
    def __init__(self, jid, password, consumer):
        super().__init__(jid, password)
        self.consumer = consumer
        self.demand = consumer.get_demand()

    async def setup(self):
        """
        Set up the DemanderAgent by adding behaviours for receiving and sending energy demand.
        """
        # print("DemanderAgent started")
        self.add_behaviour(self.ReceiveGeneration())
        self.add_behaviour(self.SendGeneration())

    class ReceiveGeneration(CyclicBehaviour):
        """
        A cyclic behaviour for receiving energy generation information from the grid controller.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "grid_controller@localhost":
                    # print(f"Demander Received {int(message.body)} message from: grid_controller.")
                    self.agent.consumer.set_generation(int(message.body))

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behaviour for sending energy demand to the grid controller.
        """
        async def run(self):
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.demand)
            await self.send(msg)
