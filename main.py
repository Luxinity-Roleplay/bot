from dis_snek import (
    Snake,
    Intents,
    listen,
    Status,
    Scale,
    slash_command,
    slash_permission,
    SlashCommandChoice,
    Permission,
    PermissionTypes,
    InteractionContext,
    slash_option,
    OptionTypes,
    context_menu,
    CommandTypes,
)

import dis_snek
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig()
cls_log = logging.getLogger(dis_snek.const.logger_name)
cls_log.setLevel(logging.DEBUG)


client = Snake(
    intents=Intents.ALL,
    sync_interactions=True,  # sync application commands with discord
    delete_unused_application_cmds=True,  # Delete commands that arent listed here
    asyncio_debug=True,  # Enable debug mode for asyncio
    debug_scope=812150001089118210,  # Override the commands scope, and only create them in this guild
)
# during testing, we recommend setting `debug_scope`, this forces your commands to only be registered in the listed guild

# load the cogs (scale)
client.grow_scale("scales.register")
client.grow_scale("scales.change")
client.grow_scale("scales.presence")
client.grow_scale("scales.setadmin")
client.grow_scale("scales.support")
client.grow_scale("scales.announce")
client.grow_scale("scales.github")
client.grow_scale("scales.ready")
client.grow_scale("scales.help")


@slash_command(
    "regrow",
    description="regrow a scale",
    scopes=[812150001089118210],
    permissions=[
        Permission(
            id=727798940430237757,
            guild_id=812150001089118210,
            type=PermissionTypes.USER,
            permission=True,
        ),
        Permission(
            id=351150966948757504,
            guild_id=812150001089118210,
            type=PermissionTypes.USER,
            permission=True,
        ),
        Permission(
            id=812150001089118210,
            guild_id=812150001089118210,
            type=PermissionTypes.ROLE,
            permission=False,
        ),
    ],
)
@slash_option(
    name="scale",
    description="the scale to regrow",
    required=True,
    opt_type=OptionTypes.STRING,
    choices=[
        SlashCommandChoice(name="Register commands", value="register"),
        SlashCommandChoice(name="UCP Change commands", value="change"),
        SlashCommandChoice(name="Set admin commands", value="setadmin"),
        SlashCommandChoice(name="Support events", value="support"),
        SlashCommandChoice(name="Presence change events", value="presence"),
        SlashCommandChoice(name="Announcement events", value="announce"),
        SlashCommandChoice(name="Github helper", value="github"),
        SlashCommandChoice(name="Ready events", value="ready"),
        SlashCommandChoice(name="Wiki commands", value="wiki"),
    ],
)
async def reload(ctx: InteractionContext, scale: str):
    client.regrow_scale(f"scales.{scale}")
    embed = dis_snek.Embed(
        description=f"<:check:839158727512293406> **{scale}** has been successfully regrown!",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    logging.info("The Bot is Ready")
    print(f"This bot is Ready to roll and owned by {client.owner}")


client.start(os.getenv("BOT_TOKEN"))
