import json
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from spade.agent import Agent


class TimeAgent(Agent):
    """
        Represents an agent that manages time and updates the environment.

        Args:
            jid (str): The agent's JID (Jabber ID).
            password (str): The password for the agent.
            env: The environment to manage.
            TIMEOUT (int): The time interval for updates.
        """
    def __init__(self, jid, password, env, TIMEOUT):
        super().__init__(jid, password)
        self.TIMEOUT = TIMEOUT
        self.time = (1, "Monday", "day")
        self.env = env

    def update_time(self):
        """
            Updates the time in the environment.
        """
        day, weekday, day_or_night = self.time
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_or_night == "day":
            self.time = (day, weekday, "night")
        else:
            self.time = (day + 1, days_of_week[(days_of_week.index(weekday) + 1) % len(days_of_week)], "day")
        self.env.current_time = self.time

    async def setup(self):
        # print("TimeControllerAgent started")
        self.add_behaviour(self.TimeUpdate(period=self.TIMEOUT))

    class TimeUpdate(PeriodicBehaviour):
        """
            Sends time updates to energy generators and sleeps for a short duration.
        """
        async def run(self):
            self.agent.update_time()
            agent_list = [
                "wind_energy_controller@localhost",
                "solar_energy_controller@localhost",
                "hydro_energy_generator@localhost",
            ]
            for agent_jid in agent_list:
                msg = Message(to=agent_jid)
                body = json.dumps(self.agent.time)
                msg.body = body
                await self.send(msg)
