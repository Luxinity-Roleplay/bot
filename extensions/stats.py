import datetime
import os
from io import BytesIO

import aiohttp
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
                values = ImageFont.truetype("assets/ARIALUNI.otf", 40)
                date_values = ImageFont.truetype("assets/ARIALUNI.otf", 35)

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

                # Draw the text

                # Nama
                draw.text(
                    (450, 255),
                    f"{name}",
                    (0, 0, 0),
                    font=values,
                )
                # Asal/Origin
                draw.text(
                    (450, 305),
                    f"{origin}",
                    (0, 0, 0),
                    font=values,
                )
                # Gender
                draw.text(
                    (450, 355),
                    f"{gender}",
                    (0, 0, 0),
                    font=values,
                )
                # Pocket
                draw.text(
                    (450, 405),
                    f"${pocket_money}",
                    (0, 0, 0),
                    font=values,
                )
                # Bank
                draw.text(
                    (450, 455),
                    f"${bank_money}",
                    (0, 0, 0),
                    font=values,
                )
                # Ingame Time
                draw.text(
                    (450, 505),
                    f"{time_hour} JAM | {time_min} MENIT | {time_hour} DETIK",
                    (0, 0, 0),
                    font=values,
                )
                # Health
                draw.text(
                    (450, 555),
                    f"{health}",
                    (0, 0, 0),
                    font=values,
                )
                # Armor
                draw.text(
                    (450, 605),
                    f"{armor}",
                    (0, 0, 0),
                    font=values,
                )
                # Expire Date
                draw.text(
                    (450, 655),
                    f"SEUMUR HIDUP",
                    (0, 0, 0),
                    font=values,
                )
                # Date
                draw.text(
                    (1195, 665),
                    f"{datetime.datetime.now().strftime('%d-%m-%Y')}",
                    (0, 0, 0),
                    font=date_values,
                )
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
    
    #leaderboards systems

    @slash_command(
        name="leaderboards",
        description="Show server leaderboards",
        group_name="rich",
        group_description="Richest leaderboards",
        sub_cmd_name="wallet",
        sub_cmd_description="Show richest characters wallet in this server",
    )
    async def lb_wallet_rich(self, ctx):
        # need to be deferred, otherwise it will be failed
        await ctx.defer()

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT * FROM characters ORDER BY Money DESC;"
                cursor.execute(sql)
                result = cursor.fetchone()

                if result is None:
                    return await ctx.send(
                        "We can't find any data in the database.",
                        ephemeral=True,
                    )
                else:
                    # create the embed
                    embed = Embed(
                        title="Server Leaderboards",
                        description="Richest characters wallet in this server",
                        color=0x00ff00,
                    )

                    # add the top 10 richest characters
                    for i in range(10):
                        embed.add_field(
                            name=f"{result['Name']}",
                            value=f"${result['Money']}",
                            inline=False,
                        )
                        result = cursor.fetchone()

                    # send the embed
                    await ctx.send(embed=embed)

    @slash_command(
        name="leaderboards",
        description="Show server leaderboards",
        group_name="rich",
        group_description="Richest leaderboards",
        sub_cmd_name="bank",
        sub_cmd_description="Show richest characters bank account in this server",
    )
    async def lb_bank_rich(self, ctx):
        # need to be deferred, otherwise it will be failed
        await ctx.defer()

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT * FROM characters ORDER BY BankMoney DESC;"
                cursor.execute(sql)
                result = cursor.fetchone()

                if result is None:
                    return await ctx.send(
                        "We can't find any data in the database.",
                        ephemeral=True,
                    )
                else:
                    # create the embed
                    embed = Embed(
                        title="Server Leaderboards",
                        description="Richest characters bank money in this server",
                        color=0x00ff00,
                    )

                    # add the top 10 richest characters
                    for i in range(10):
                        embed.add_field(
                            name=f"{result['Name']}",
                            value=f"${result['BankMoney']}",
                            inline=False,
                        )
                        result = cursor.fetchone()

                    # send the embed
                    await ctx.send(embed=embed)
    
    @slash_command(
        name="leaderboards",
        description="Show server leaderboards",
        sub_cmd_name="level",
        sub_cmd_description="Show highest level in this server",
    )
    async def lb_level(self, ctx):
        # need to be deferred, otherwise it will be failed
        await ctx.defer()

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT * FROM characters ORDER BY Level DESC;"
                cursor.execute(sql)
                result = cursor.fetchone()

                if result is None:
                    return await ctx.send(
                        "We can't find any data in the database.",
                        ephemeral=True,
                    )
                else:
                    # create the embed
                    embed = Embed(
                        title="Server Leaderboards",
                        description="Highest Character Level in this server",
                        color=0x00ff00,
                    )

                    # add the top 10 richest characters
                    for i in range(10):
                        embed.add_field(
                            name=f"{result['Name']}",
                            value=f"${result['Level']}",
                            inline=False,
                        )
                        result = cursor.fetchone()

                    # send the embed
                    await ctx.send(embed=embed)


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    stats(bot)
