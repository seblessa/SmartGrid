import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class GreenPowerControllerAgent(Agent):
    """
    Represents an agent that controls and communicates green energy information.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
    """
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        """
        Set up the GreenPowerControllerAgent by adding a cyclic behavior for communication.
        """
        # print("GreenPowerControllerAgent started")
        self.add_behaviour(self.Comunication())

    class Comunication(CyclicBehaviour):
        """
        A cyclic behavior for receiving and forwarding green energy information to the grid controller.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "wind_energy_controller@localhost":
                    # print(f"Green Power Received {int(message.body)} message from: wind_generation.")
                    msg = Message(to="grid_controller@localhost")
                    msg.body = message.body
                    await self.send(msg)
                elif message_author == "solar_energy_controller@localhost":
                    # print(f"Green Power Received {int(message.body)} message from: solar_generation.")
                    msg = Message(to="grid_controller@localhost")
                    msg.body = message.body
                    await self.send(msg)
                elif message_author == "hydro_energy_generator@localhost":
                    # print(f"Green Power Received {int(message.body)} message from: hydro_generation.")
                    msg = Message(to="grid_controller@localhost")
                    msg.body = message.body
                    await self.send(msg)
                else:
                    print(f"Green Energy Agent Received '{message.body}' message from: {message_author}.")
