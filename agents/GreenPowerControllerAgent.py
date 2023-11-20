import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class GreenPowerControllerAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    async def setup(self):
        # print("GreenPowerControllerAgent started")
        self.add_behaviour(self.Comunication())

    class Comunication(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "wind_energy_controller@localhost":
                    # print(f"Green Power Received {json.loads(message.body).get("wind_generation")} message from: wind_generation.")
                    received_data = json.loads(message.body)
                    data_to_send = {"wind_generation": received_data.get("wind_generation")}
                    data_string = json.dumps(data_to_send)
                    msg = Message(to="grid_controller@localhost")
                    msg.body = data_string
                    await self.send(msg)
                elif message_author == "solar_energy_controller@localhost":
                    # print(f"Green Power Received {json.loads(message.body).get("solar_generation")} message from: solar_generation.")
                    received_data = json.loads(message.body)
                    data_to_send = {"solar_generation": received_data.get("solar_generation")}
                    data_string = json.dumps(data_to_send)
                    msg = Message(to="grid_controller@localhost")
                    msg.body = data_string
                    await self.send(msg)
                elif message_author == "hydro_energy_generator@localhost":
                    # print(f"Green Power Received {json.loads(message.body).get("hydro_generation")} message from: hydro_generation.")
                    received_data = json.loads(message.body)
                    data_to_send = {"hydro_generation": received_data.get("hydro_generation")}
                    data_string = json.dumps(data_to_send)
                    msg = Message(to="grid_controller@localhost")
                    msg.body = data_string
                    await self.send(msg)
                else:
                    print(f"Green Energy Agent Received '{message.body}' message from: {message_author}.")
