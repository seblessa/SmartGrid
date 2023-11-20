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
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.__generation = 0
        self.__limit = 25000

    def set_generation(self, generation):
        """
        Sets the energy generation level for the fossil fuel generator.

        Args:
            generation (int): The energy generation level.
        """
        self.__generation = generation

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
                    # print(f"Fossil Fuel Generator Received {message.body} message from: grid_controller.")
                    energy_needed = int(message.body)
                    self.agent.set_generation(min(energy_needed, self.agent.__limit))
                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                    await send_behaviour.wait()
                else:
                    print(f"Fossil Fuel Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        """
        A one-shot behavior for sending the generated energy to the grid controller.
        """
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="grid_controller@localhost")
            msg.body = str(self.agent.__generation)
            await self.send(msg)
