from dis_snek import (
    Scale,
    Button,
    ButtonStyles,
    InteractionContext,
    AutoArchiveDuration,
    ChannelTypes,
    Permission,
    PermissionTypes,
    listen,
    slash_command,
    ActionRow,
)
from dotenv import load_dotenv
from github import Github

import dis_snek
import os


load_dotenv()

server_id = 812150001089118210
rtc = 850304670966743050
rtc_msg = 971799833734156291

client = Github(os.getenv("GITHUB_TOKEN"))
# read-this-channel
gist = client.get_gist(os.getenv("GIST_ID"))
first_file = list(gist.files.values())[0]
results = first_file.raw_data["content"]


class ready(Scale):
    @listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
    async def on_ready(self):
        server = self.bot.get_guild(server_id)
        # read-this channel
        rtc_channel = await server.fetch_channel(rtc)
        rtc_text = await rtc_channel.fetch_message(rtc_msg)

        embed = dis_snek.Embed(
            description=f"{results}",
            color=0x3874FF,
        )
        embed.set_thumbnail(url=server.icon.url)
        await rtc_text.edit(
            embed=embed,
            components=[
                Button(
                    style=ButtonStyles.BLURPLE,
                    label="Click here to take @Players role!",
                    custom_id="assign_role",
                    emoji="<:Luxinity:971789146492395591>",
                )
            ],
        )

    @listen()
    async def on_button(self, b):
        ctx = b.context
        if ctx.custom_id == "assign_role":
            await ctx.defer(ephemeral=True)
            ping_id = 846706127021932544
            if ctx.author.has_role(ping_id):
                return await ctx.send(
                    f"😕 You're already have <@&{ping_id}> role!", ephemeral=True
                )
            else:
                await ctx.author.add_role(ping_id, "User requested to add role")
                return await ctx.send(
                    f"The <@&{ping_id}> role has been added", ephemeral=True
                )


def setup(bot):
    ready(bot)
