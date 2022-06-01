from naff import listen, Extension, Status
from naff.models.naff.tasks import Task
from naff.models.naff.tasks.triggers import IntervalTrigger
from samp_client.client import SampClient
from dotenv import load_dotenv

import os
import naff

load_dotenv()


class presence(Extension):
    @Task.create(IntervalTrigger(seconds=10))
    async def ganti(self):
        try:
            ip = os.getenv("IP")
            port = os.getenv("PORT")
            with SampClient(address=ip, port=port) as kung:
                info = kung.get_server_info()
            await self.bot.change_presence(
                status=Status.ONLINE,
                activity=f"with {info.players}/{info.max_players} Players",
            )
        except:
            await self.bot.change_presence(
                status=Status.DND,
                activity="Server is Offline!",
            )

    @listen()  # this decorator tells naff that it needs to listen for the corresponding event, and run this coroutine
    async def on_ready(self):
        self.ganti.start()
        try:
            ip = os.getenv("IP")
            port = os.getenv("PORT")
            with SampClient(address=ip, port=port) as kung:
                info = kung.get_server_info()
            await self.bot.change_presence(
                status=Status.ONLINE,
                activity=f"with {info.players}/{info.max_players} Players",
            )
        except:
            await self.bot.change_presence(
                status=Status.DND,
                activity="Server is Offline!",
            )


def setup(bot):
    # This is called by dis-naff so it knows how to load the Extension
    presence(bot)
