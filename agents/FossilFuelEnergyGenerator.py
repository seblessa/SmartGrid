from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class FossilFuelEnergyGenerator(Agent):
    """
    Represents an agent that generates energy using fossil fuel.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """
    def __init__(self, jid, password, generator):
        super().__init__(jid, password)
        self.generator = generator
        self.generation = 0
        self.limit = 500000000

    async def setup(self):
        """
        Set up the FossilFuelEnergyGenerator agent by adding a behavior for updating energy generation.
        """
        # print("Solar Generator started")
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        """
        A cyclic behavior for updating energy generation based on the energy demand from the grid controller.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "grid_controller@localhost":
                    # print(f"Fossil Fuel Generator received {message.body} from: grid_controller.")
                    energy_needed = int(message.body)
                    self.agent.generation = min(energy_needed, self.agent.limit)
                    self.agent.generator.set_generation(self.agent.generation)

                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                else:
                    print(f"Fossil Fuel Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending the generated energy to the grid controller.
        """
        async def run(self):
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.generation)
            # print(f"Sending {msg.body} fossil fuel generation produced to {msg.to}!")
            await self.send(msg)
