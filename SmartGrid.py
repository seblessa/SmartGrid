from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class SmartGridAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.environment = None

    def send_message(self, receiver, message):
        class SendMessageBehaviour(OneShotBehaviour):
            async def run(self):
                msg = Message(to=receiver)
                msg.body = message
                await self.send(msg)

        self.add_behaviour(SendMessageBehaviour())

    def receive_message(self, timeout=10):
        class ReceiveMessageBehaviour(OneShotBehaviour):
            async def run(self):
                msg = await self.receive(timeout=timeout)
                if msg:
                    print(f"Received message: {msg.body}")
                else:
                    print(f"Did not receive any message after {timeout} seconds")

        self.add_behaviour(ReceiveMessageBehaviour())
