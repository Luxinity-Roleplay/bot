import logging
import os
import sys

import naff
from dotenv import load_dotenv
from naff import (
    Activity,
    ActivityType,
    Client,
    CommandTypes,
    Embed,
    Intents,
    InteractionContext,
    OptionTypes,
    Permissions,
    PrefixedContext,
    SlashCommandChoice,
    Status,
    check,
    context_menu,
    listen,
    prefixed_command,
    slash_command,
    slash_option,
)

from utilities.checks import *

load_dotenv()

client = Client(
    intents=Intents.ALL,
    sync_interactions=True,  # sync application commands with discord
    delete_unused_application_cmds=True,  # Delete commands that arent listed here
    debug_scope=812150001089118210,  # Override the commands scope, and only create them in this guild
)
# during testing, we recommend setting `debug_scope`, this forces your commands to only be registered in the listed guild

# load the Extensions (scale)
for root, dirs, files in os.walk("scales"):
    for file in files:
        if file.endswith(".py") and not file.startswith("__init__"):
            file = file.removesuffix(".py")
            path = os.path.join(root, file)
            python_import_path = path.replace("/", ".").replace("\\", ".")

            # load the scale
            client.load_extension(python_import_path)


@prefixed_command(name="load")
@check(is_owner())
async def load(ctx: PrefixedContext, scale: str):
    client.load_extension(f"scales.{scale}")
    embed = Embed(
        description=f"<:check:839158727512293406> **{scale}** has been successfully growed!",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)


@prefixed_command(name="unload")
@check(is_owner())
async def unload(ctx: PrefixedContext, scale: str):
    client.unload_extension(f"scales.{scale}")
    embed = Embed(
        description=f"<:check:839158727512293406> **{scale}** has been successfully ungrowed!",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)


@prefixed_command(name="reload")
@check(is_owner())
async def reload(ctx: PrefixedContext, scale: str):
    client.reload_extension(f"scales.{scale}")
    embed = Embed(
        description=f"<:check:839158727512293406> **{scale}** has been successfully regrowed!",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@prefixed_command(name="reboot")
@check(is_owner())
async def reboot(ctx: PrefixedContext):
    embed = Embed(
        description=f":wave: The bot has been Rebooting, Please Wait..",
        color=0xE74C3C,
    )
    await ctx.send(embed=embed)
    restart_program()


@prefixed_command(name="shutdown")
@check(is_owner())
async def shutdown(ctx: PrefixedContext):
    embed = Embed(
        description=f":wave: The bot has been Shutdowned, Goodbye World.",
        color=0xE74C3C,
    )
    await ctx.send(embed=embed)
    await client.stop()


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    logging.info("The Bot is Ready")
    print(f"This bot is Ready to roll and owned by {client.owner}")


client.start(os.getenv("BOT_TOKEN"))
