from dis_snek import listen, Scale, Status
from dis_snek.models.snek.tasks import Task
from dis_snek.models.snek.tasks.triggers import IntervalTrigger
from samp_client.client import SampClient
from dotenv import load_dotenv

import os
import dis_snek

load_dotenv()


class presence(Scale):
    ip = os.getenv("IP")
    port = os.getenv("PORT")

    @Task.create(IntervalTrigger(seconds=10))
    async def ganti(self):
        with SampClient(address=ip, port=port) as kung:
            info = kung.get_server_info()
        await self.bot.change_presence(
            status=Status.ONLINE,
            activity=f"with {info.players}/{info.max_players} Players",
        )

    @listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
    async def on_ready(self):
        self.ganti.start()
        with SampClient(address=ip, port=port) as kung:
            info = kung.get_server_info()
        await self.bot.change_presence(
            status=Status.ONLINE,
            activity=f"with {info.players}/{info.max_players} Players",
        )


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    presence(bot)
