import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message


class WindEnergyGenerator(Agent):
    def __init__(self, jid, password):
        print("***")
        super().__init__(jid, password)
        self.__values = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
        self.__wind_generation = self.__values[0]

    def set_generation(self, generation):
        self.__wind_generation = generation

    async def setup(self):
        # print("Wind Generator started")
        self.add_behaviour(self.UpdateGeneration())

    class UpdateGeneration(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                message_author = str(message.sender)
                # print("Received message!")
                if message_author == "time_controller@localhost":
                    # print(f"WindEnergyController Received {message.body} message from: time_controller.")
                    day, week_day, day_or_night = message.body

                    choice = random.choice((
                        max(0, self.agent.__values.index(self.agent.__wind_generation) - 1),
                        min(len(self.agent.__values) - 1, self.agent.__values.index(self.agent.__wind_generation) + 1)))

                    if day_or_night == "day":
                        self.agent.set_generation(choice)
                    else:  # day_or_night == "night":
                        self.agent.set_generation(choice * 1.5)

                    send_behaviour = self.agent.SendGeneration()
                    self.agent.add_behaviour(send_behaviour)
                    await send_behaviour.wait()
                else:
                    print(f"Wind Energy Generator Received '{message.body}' message from: {message_author}.")

    class SendGeneration(OneShotBehaviour):
        async def run(self):
            # print("Sending all wind generation produced!")
            msg = Message(to="wind_energy_controller@localhost")
            msg.body = str(self.agent.__wind_generation)
            await self.send(msg)