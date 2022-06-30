import datetime
import os

import naff
import pymysql.cursors
from dotenv import load_dotenv
from millify import prettify
from naff import (AutocompleteContext, Button, ButtonStyles, Embed, Extension,
                  MessageTypes, OptionTypes, Permissions, PrefixedContext,
                  check, listen, prefixed_command, slash_command, slash_option)

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
        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if character is already registered
                sql = f"SELECT * FROM `characters` WHERE `Name`=%s"
                cursor.execute(sql, (name))
                result = cursor.fetchone()

                if result is None:
                    return await ctx.send("We can't find that character on our system, Please check for typo's or try to create a character!", ephemeral=True)
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
                    
                    # define the embed
                    embed = Embed(color=0x00FF00)
                    embed.set_author(
                        name=f"{name}'s Stats",
                        icon_url=ctx.guild.icon.url,
                    )
                    embed.add_field(name="Character Name:", value=f"{name}", inline=False)
                    embed.add_field(name="UCP Account:", value=f"{ucp}", inline=False)
                    embed.add_field(name="Gender:", value=f"{gender}", inline=True)
                    embed.add_field(name="Age:", value=f"{age}", inline=True)
                    embed.add_field(name="Origin:", value=f"{origin}", inline=True)
                    embed.add_field(name="Health:", value=f"{health}%", inline=True)
                    embed.add_field(name="Armor:", value=f"{armor}", inline=True)
                    embed.add_field(name="Level:", value=f"{level}", inline=True)
                    embed.add_field(name="In-game:", value=f"{time_hour} **Hour(s)** {time_min} **Minute(s)** {time_hour} **Second(s)**", inline=False)
                    embed.add_field(name="Money:", value=f"Pocket: **$**{pocket_money} | Bank: **$**{bank_money}", inline=False)
                    embed.set_image(url=f"https://assets.open.mp/assets//images/skins/{skin}.png")
                    embed.set_footer(
                        text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
                    )
                    embed.timestamp = datetime.datetime.utcnow()

                    # send the embed
                    return await ctx.send(embed=embed)

def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    stats(bot)
