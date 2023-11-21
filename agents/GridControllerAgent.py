import asyncio

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
        self.neighborhood_demand = 0
        self.neighbours_demand = 0
        self.hospital_demand = 0
        self.police_demand = 0
        self.firefighters_demand = 0

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
                    # print(f"GridControllerAgent received {int(message.body)} from {message_author}")
                    self.agent.generation += int(message.body)

                elif message_author == "fossil_fuel_power_generator@localhost":
                    # print(f"Grid Agent received {message.body} from {message_author}")
                    self.agent.generation += int(message.body)

                elif message_author == "neighborhood_controller@localhost":
                    # print(f"Grid Agent received {message.body} from {message_author}")
                    self.agent.neighborhood_demand = int(message.body)

                elif message_author == "hospital_demander@localhost":
                    # print(f"Grid Agent received {message.body} from {message_author}")
                    self.agent.hospital_demand = int(message.body)

                elif message_author == "police_station_demander@localhost":
                    # print(f"Grid Agent received {message.body} from {message_author}")
                    self.agent.police_demand = int(message.body)

                elif message_author == "fire_station_demander@localhost":
                    # print(f"Grid Agent received {message.body} from {message_author}")
                    self.agent.firefighters_demand = int(message.body)

                else:
                    print(f"Grid Agent Received '{message.body}' message from: {message_author}.")

                await asyncio.sleep(1)
                self.agent.add_behaviour(self.agent.SendingData())

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

            min_gen = min(self.agent.hospital_demand, self.agent.generation)
            self.agent.generation = max(0, self.agent.generation - min_gen)
            msg_to_hospital = Message(to="hospital_demander@localhost")
            msg_to_hospital.body = str(min_gen)
            await self.send(msg_to_hospital)
            # print(f"Grid Agent sent a message to {msg_to_hospital.to}!")

            min_gen = min(self.agent.firefighters_demand, self.agent.generation)
            self.agent.generation = max(0, self.agent.generation - min_gen)
            msg_to_firefighters = Message(to="fire_station_demander@localhost")
            msg_to_firefighters.body = str(min_gen)
            await self.send(msg_to_firefighters)
            # print(f"Grid Agent sent a message to {msg_to_firefighters.to}!")

            min_gen = min(self.agent.police_demand, self.agent.generation)
            self.agent.generation = max(0, self.agent.generation - min_gen)
            msg_to_police = Message(to="police_station_demander@localhost")
            msg_to_police.body = str(min_gen)
            await self.send(msg_to_police)
            # print(f"Grid Agent sent a message to {msg_to_police.to}!")

            min_gen = min(self.agent.neighborhood_demand, self.agent.generation)
            self.agent.generation = max(0, self.agent.generation - min_gen)
            msg_to_neighborhood = Message(to="neighborhood_controller@localhost")
            msg_to_neighborhood.body = str(min_gen)
            await self.send(msg_to_neighborhood)
            # print(f"Grid Agent sent a message to {msg_to_neighborhood.to}!")

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
            # print(f"Grid Agent sent a message to {msg.to}!")
