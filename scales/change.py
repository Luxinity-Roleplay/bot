from naff import (
    slash_command,
    Modal,
    ShortText,
    cooldown,
    Buckets,
    Extension,
    Embed
)
from dotenv import load_dotenv

import os
import logging
import bcrypt
import pymysql.cursors
import datetime

load_dotenv()

# Connect to the database
connection = pymysql.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME"),
    cursorclass=pymysql.cursors.DictCursor,
)


class change(Extension):
    @slash_command(
        "change-username", description="Ganti username UCP anda gapake ribeddd!"
    )
    async def change_user(self, ctx):
        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if user is already registered
                sql = f"SELECT `discord_userid` FROM `playerucp` WHERE `discord_userid`=%s"
                cursor.execute(sql, (ctx.author.id))
                result = cursor.fetchone()

                if result is not None:
                    my_modal = Modal(
                        title="Change Username UCP Luxinity Roleplay",
                        components=[
                            ShortText(
                                label="Username",
                                custom_id="username",
                                placeholder="Masukkan username baru UCP kamu!",
                                required=True,
                            ),
                        ],
                    )
                    await ctx.send_modal(modal=my_modal)  # send modal to users

                    # wait for user to enter the credentials
                    modal_ctx: ModalContext = await self.bot.wait_for_modal(my_modal)

                    # get channel to send the logs
                    w = self.bot.get_channel(966685759832723476)

                    # get modal responses
                    usern = modal_ctx.responses["username"]

                    # add records to database
                    sql = "UPDATE `playerucp` SET `UCP` = %s WHERE `playerucp`.`discord_userid` = %s"
                    cursor.execute(sql, (f"{usern}", f"{ctx.author.id}"))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()

                    # send embed to ucp-logs
                    embed = Embed(
                        title="UCP Username changed!", color=0x00FF00
                    )
                    embed.add_field(
                        name="New Username:", value=f"{usern}", inline=False
                    )
                    embed.set_author(
                        name=f"{ctx.author.username}#{ctx.author.discriminator}",
                        url=f"https://discordapp.com/users/{ctx.author.id}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_thumbnail(url=ctx.author.avatar.url)
                    embed.set_footer(
                        text=f"{ctx.guild.name} | User ID: {ctx.author.id}",
                        icon_url=ctx.guild.icon.url,
                    )
                    embed.timestamp = datetime.datetime.utcnow()
                    await w.send(embed=embed)

                    # send username & password to user for safekeeping
                    manusya = Embed(
                        description="**Your New UCP Username**", color=0x17A168
                    )
                    manusya.add_field(name="Username:", value=f"{usern}", inline=False)
                    try:
                        await ctx.author.send(embed=manusya)
                        await modal_ctx.send(
                            "Successfully changed your UCP Username.\n\nCheck your DM's for your new Username!",
                            ephemeral=True,
                        )
                    except:
                        logging.info(f"Can't send message to {ctx.author} :(")
                        await modal_ctx.send(
                            "Successfully changed your UCP Username.\n\nUnfortunately your server dm's are closed and we can't send your new Username :(",
                            ephemeral=True,
                        )
                else:
                    # send error message if user already registered
                    await ctx.send(
                        "We can't find your UCP account!\n\nPlease register first using `/register`!",
                        ephemeral=True,
                    )

    @slash_command(
        "change-password", description="Ganti password UCP anda gapake ribeddd!"
    )
    async def change_pass(self, ctx):
        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if user is already registered
                sql = f"SELECT `discord_userid` FROM `playerucp` WHERE `discord_userid`=%s"
                cursor.execute(sql, (ctx.author.id))
                result = cursor.fetchone()

                if result is not None:
                    my_modal = Modal(
                        title="Change Password UCP Luxinity Roleplay",
                        components=[
                            ShortText(
                                label="Password",
                                custom_id="password",
                                placeholder="Masukkan password baru UCP kamu!",
                                required=True,
                            ),
                        ],
                    )
                    await ctx.send_modal(modal=my_modal)  # send modal to users

                    # wait for user to enter the credentials
                    modal_ctx: ModalContext = await self.bot.wait_for_modal(my_modal)

                    # get channel to send the logs
                    w = self.bot.get_channel(966685759832723476)

                    # get modal responses
                    passwd = modal_ctx.responses["password"]

                    # hash passwords
                    hashed = bcrypt.hashpw(
                        passwd.encode("utf8"), bcrypt.gensalt()
                    ).decode("utf8")

                    # add records to database
                    sql = "UPDATE `playerucp` SET `Password` = %s WHERE `playerucp`.`discord_userid` = %s"
                    cursor.execute(sql, (f"{hashed}", f"{ctx.author.id}"))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()

                    # send embed to ucp-logs
                    embed = Embed(
                        title="UCP Password changed!", color=0x00FF00
                    )
                    embed.add_field(
                        name="New Hashed Password:", value=f"||{hashed}||", inline=False
                    )
                    embed.set_author(
                        name=f"{ctx.author.username}#{ctx.author.discriminator}",
                        url=f"https://discordapp.com/users/{ctx.author.id}",
                        icon_url=ctx.author.avatar.url,
                    )
                    embed.set_thumbnail(url=ctx.author.avatar.url)
                    embed.set_footer(
                        text=f"{ctx.guild.name} | User ID: {ctx.author.id}",
                        icon_url=ctx.guild.icon.url,
                    )
                    embed.timestamp = datetime.datetime.utcnow()
                    await w.send(embed=embed)

                    # send username & password to user for safekeeping
                    manusya = Embed(
                        description="**Your New UCP Password**", color=0x17A168
                    )
                    manusya.add_field(
                        name="Password:", value=f"||{passwd}||", inline=False
                    )
                    try:
                        await ctx.author.send(embed=manusya)
                        await modal_ctx.send(
                            "Successfully changed your UCP Password.\n\nCheck your DM's for your Password!\nTo reset your password again, please use `/change-password` commands.",
                            ephemeral=True,
                        )
                    except:
                        logging.info(f"Can't send message to {ctx.author} :(")
                        await modal_ctx.send(
                            "Successfully changed your UCP Password.\n\nUnfortunately your server dm's are closed and we can't send your new Password :(\nTo reset your password again, please use `/change-password` commands.",
                            ephemeral=True,
                        )
                else:
                    # send error message if user already registered
                    await ctx.send(
                        "We can't find your UCP account!\n\nPlease register first using `/register`!",
                        ephemeral=True,
                    )


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    change(bot)
