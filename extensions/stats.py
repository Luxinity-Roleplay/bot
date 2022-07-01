import datetime
import os

import aiohttp
from io import BytesIO
import naff
import pymysql.cursors
from dotenv import load_dotenv
from millify import prettify
from naff import (
    AutocompleteContext,
    Button,
    ButtonStyles,
    Embed,
    Extension,
    MessageTypes,
    OptionTypes,
    Permissions,
    PrefixedContext,
    check,
    listen,
    prefixed_command,
    slash_command,
    slash_option,
)
from PIL import Image, ImageDraw, ImageFont

from utilities.checks import *

load_dotenv()

# Connect to the database
connection = pymysql.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME"),
    cursorclass=pymysql.cursors.DictCursor,
)


class stats(Extension):
    @slash_command(
        "stats",
        description="Show a player character stats",
    )
    @slash_option(
        name="name",
        description="The target character's name, e.g. 'Firpan_Pus'",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def stats(self, ctx, name=str):
        # need to be deferred, otherwise it will be failed
        await ctx.defer()

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT * FROM `characters` WHERE `Name`=%s"
                cursor.execute(sql, (name))
                result = cursor.fetchone()

                if result is None:
                    return await ctx.send(
                        "We can't find that character on our system, Please check for typo's or try to create a character!",
                        ephemeral=True,
                    )
                else:
                    # define things we want to use
                    name = result["Name"]

                    health = int(result["Health"])
                    if health == 0:
                        health = "Player is dead"

                    armor = int(result["Armor"])
                    if armor == 0:
                        armor = "No Armor"
                    else:
                        armor = f"{armor}%"

                    ucp = result["UCP"]

                    age = result["Age"]

                    origin = result["Origin"]

                    gender = result["Gender"]
                    if gender == 0:
                        gender = "Male"
                    else:
                        gender = "Female"

                    skin = result["Skin"]

                    pocket_money = prettify(result["Money"])
                    bank_money = prettify(result["BankMoney"])

                    level = result["Level"]

                    time_hour = result["Hours"]
                    time_min = result["Minutes"]
                    time_sec = result["Second"]

                # Replace blanko.png with your background image.
                img = Image.open("assets/blanko.png")
                draw = ImageDraw.Draw(img)
                # Make sure you insert a valid font from your folder.
                values = ImageFont.truetype("assets/ARIALUNI.otf", 70)

                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://assets.open.mp/assets//images/skins/{skin}.png"
                    ) as response:
                        image = await response.read()
                avatar = (
                    Image.open(BytesIO(image))
                    .resize((300, 390), Image.LANCZOS)
                    .convert("RGB")
                )
                img.paste(avatar, (1135, 240))

                # Save our files.
                img.save(f"assets/card.png")
                ffile = naff.File(f"assets/card.png")
                return await ctx.send(
                    f"{ctx.author.mention}, Here's [`{name}`] character stats",
                    file=ffile,
                )

    @stats.autocomplete("name")
    async def stats_autocomplete(self, ctx: AutocompleteContext, name: str):
        choices = []

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT `Name` FROM `characters` WHERE `Name`=%s"
                cursor.execute(sql, (name))

                for Name in cursor:
                    choices.append({"name": f"{name}", "value": f"{name}"})
                    await ctx.send(choices=choices)


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    stats(bot)
