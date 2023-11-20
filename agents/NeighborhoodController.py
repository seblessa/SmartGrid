from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class NeighborhoodController(Agent):
    """
    Represents an agent that manages energy demand and distribution for multiple neighborhoods.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
        neighborhoods (list): List of neighborhoods associated with the controller.
    """
    def __init__(self, jid, password, neighborhoods):
        super().__init__(jid, password)
        self.__neighborhoods = neighborhoods
        self.__demand = sum([neighborhood.get_demand() for neighborhood in self.__neighborhoods])

    async def setup(self):
        """
        Set up the NeighborhoodController agent by adding behaviors for receiving and sending energy generation information.
        """
        # print("DemanderAgent started")
        self.add_behaviour(self.ReceiveGeneration())
        self.add_behaviour(self.SendGeneration())

    class ReceiveGeneration(CyclicBehaviour):
        """
        A cyclic behavior for receiving energy generation information from the grid controller and updating neighborhoods.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "grid_controller@localhost":
                    # print(f"Neighborhood Controller Received {int(message.body)} message from: grid_controller.")
                    generation = int(message.body)
                    for neighborhood in self.agent.__neighborhoods:
                        min_gen = min(neighborhood.get_demand(), generation)
                        generation = max(0, generation - min_gen)
                        neighborhood.update_generation(min_gen)

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending total energy demand to the grid controller.
        """
        async def run(self):
            # print("Sending demand!")
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.__demand)
            await self.send(msg)
