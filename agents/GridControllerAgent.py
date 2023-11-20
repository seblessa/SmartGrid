import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class GridControllerAgent(Agent):
    """
    Represents an agent that controls the distribution of energy among different entities.

    Args:
        jid (str): The agent's JID (Jabber ID).
        password (str): The password for the agent.
        env: The environment associated with the agent.
    """
    def __init__(self, jid, password, env):
        super().__init__(jid, password)
        self.env = env
        self.generation = 0
        self.green_message = False
        self.ff_message = False
        self.neighborhood_message = True
        self.hospital_message = False
        self.police_message = False
        self.firefighters_message = False
        self.neighborhood_demand = 0
        self.neighbours_demand = 0
        self.hospital_demand = 0
        self.police_demand = 0
        self.firefighters_demand = 0

    def all_messages_received(self):
        """
        Checks if all the necessary messages from different entities are received.

        Returns:
            bool: True if all messages are received, False otherwise.
        """
        return self.green_message and self.ff_message and self.hospital_message and self.police_message and self.firefighters_message and self.neighborhood_message

    def get_demand(self):
        """
            Calculates the total energy demand from all entities.

            Returns:
                int: The total energy demand.
        """
        return self.neighbours_demand + self.hospital_demand + self.police_demand + self.firefighters_demand

    async def setup(self):
        """
        Set up the GridControllerAgent by adding a cyclic behavior for receiving data.
        """
        # print("GridControllerAgent started")
        self.add_behaviour(self.ReceivingData())

    class ReceivingData(CyclicBehaviour):
        """
        A cyclic behavior for receiving data from different entities and updating energy generation.
        """
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                if message_author == "green_power_controller@localhost":
                    self.agent.green_message = True
                    self.agent.generation = 0

                    received_data = json.loads(message.body)

                    for key, value in received_data.items():
                        if key == "wind_generation":
                            self.agent.generation += int(value)
                        elif key == "solar_generation":
                            self.agent.generation += int(value)
                        elif key == "hydro_generation":
                            self.agent.generation += int(value)

                elif message_author == "fossil_fuel_power_generator@localhost":
                    self.agent.ff_message = True
                    self.agent.generation += int(message.body)

                elif message_author == "neighborhood_controller@localhost":
                    self.agent.neighborhood_message = True
                    self.agent.neighborhood_demand = int(message.body)

                elif message_author == "hospital_demander@localhost":
                    self.agent.hospital_message = True
                    self.agent.hospital_demand = int(message.body)

                elif message_author == "police_station_demander@localhost":
                    self.agent.police_message = True
                    self.agent.police_demand = int(message.body)

                elif message_author == "fire_station_demander@localhost":
                    self.agent.firefighters_message = True
                    self.agent.firefighters_demand = int(message.body)
                    pass

                else:
                    print(f"Grid Agent Received '{message.body}' message from: {message_author}.")

            # Check priority order to send energy
            if self.agent.all_messages_received():
                sending_behav = self.agent.SendingData()
                self.agent.add_behaviour(sending_behav)
                await sending_behav.wait()

    class SendingData(OneShotBehaviour):
        """
        A one-shot behavior for sending energy to different entities based on priority.
        """
        async def run(self):
            if self.agent.generation < self.agent.get_demand():
                # Not enough energy to supply all demand
                energy_needed = self.agent.get_demand() - self.agent.generation
                request_energy_behav = self.agent.RequestMoreEnergy(energy_needed)
                self.agent.add_behaviour(request_energy_behav)
                await request_energy_behav.wait()

            generation = self.agent.generation

            min_gen = min(self.agent.hospital_demand, generation)
            generation = max(0, generation - min_gen)
            msg_to_hospital = Message(to="hospital_demander@localhost")
            msg_to_hospital.body = str(min_gen)
            await self.send(msg_to_hospital)

            min_gen = min(self.agent.firefighters_demand, generation)
            generation = max(0, generation - min_gen)
            msg_to_firefighters = Message(to="fire_station_demander@localhost")
            msg_to_firefighters.body = str(min_gen)
            await self.send(msg_to_firefighters)

            min_gen = min(self.agent.police_demand, generation)
            generation = max(0, generation - min_gen)
            msg_to_police = Message(to="police_station_demander@localhost")
            msg_to_police.body = str(min_gen)
            await self.send(msg_to_police)

            min_gen = min(self.agent.neighborhood_demand, generation)
            # generation = max(0, generation - min_gen)
            msg_to_neighborhood = Message(to="neighborhood_controller@localhost")
            msg_to_neighborhood.body = str(min_gen)
            await self.send(msg_to_neighborhood)

    class RequestMoreEnergy(OneShotBehaviour):
        """
        A one-shot behavior for requesting more energy from the fossil fuel power generator.
        """
        def __init__(self, energy_needed):
            super().__init__()
            self.energy_needed = energy_needed

        async def run(self):
            msg = Message(to="fossil_fuel_power_generator@localhost")
            msg.body = str(self.energy_needed)
            await self.send(msg)
            # print(f"Grid Controller Agent requested {self.energy_needed} more energy to fossil fuel power generator.")
