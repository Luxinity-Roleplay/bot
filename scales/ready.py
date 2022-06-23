import datetime
import logging
import os

import bcrypt
import naff
import pymysql.cursors
from dotenv import load_dotenv
from github import Github
from naff import (
    ActionRow,
    AutoArchiveDuration,
    Buckets,
    Button,
    ButtonStyles,
    ChannelTypes,
    Embed,
    Extension,
    InteractionContext,
    Modal,
    ShortText,
    cooldown,
    listen,
    slash_command,
)

load_dotenv()

server_id = 812150001089118210
rtc = 850304670966743050
rtc_msg = 971799833734156291

acc = 967246558745722970
acc_msg = 989592998813790240

client = Github(os.getenv("GITHUB_TOKEN"))

# read-this-channel
gist = client.get_gist(os.getenv("GIST_ID"))
first_file = list(gist.files.values())[0]
results = first_file.raw_data["content"]

# account-manager
gist2 = client.get_gist(os.getenv("GIST_ID2"))
second_file = list(gist2.files.values())[0]
results2 = second_file.raw_data["content"]


class ready(Extension):
    @listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
    async def on_ready(self):
        server = self.bot.get_guild(server_id)
        # read-this-channel
        rtc_channel = await server.fetch_channel(rtc)
        rtc_text = await rtc_channel.fetch_message(rtc_msg)

        # account-manager
        acc_channel = await server.fetch_channel(acc)
        acc_text = await acc_channel.fetch_message(acc_msg)

        embed1 = Embed(color=0x00FF00)
        embed1.title = "Account Manager"
        embed1.description = results2
        embed1.set_footer(
            text=f"{server.name}",
            icon_url=server.icon.url,
        )
        await acc_text.edit(
            embed=embed1,
            components=[
                Button(
                    style=ButtonStyles.GREEN,
                    label="Register Account",
                    custom_id="register",
                    emoji="📋",
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    label="Change Username",
                    custom_id="user",
                    emoji="🤔",
                ),
                Button(
                    style=ButtonStyles.DANGER,
                    label="Change/Forget Password",
                    custom_id="password",
                    emoji="🔑",
                ),
            ],
        )

        embed = Embed(
            description=f"{results}",
            color=0x3874FF,
        )
        embed.set_thumbnail(url=server.icon.url)
        await rtc_text.edit(
            embed=embed,
            components=[
                Button(
                    style=ButtonStyles.BLURPLE,
                    label="I accept the Server Rules",
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

        if ctx.custom_id == "register":
            # Connect to the database
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
            )
            # ping the mysql server
            connection.ping(reconnect=True)

            with connection:
                with connection.cursor() as cursor:
                    # check if user is already registered
                    sql = f"SELECT `discord_userid` FROM `playerucp` WHERE `discord_userid`=%s"
                    cursor.execute(sql, (ctx.author.id))
                    result = cursor.fetchone()

                    if result is None:
                        my_modal = Modal(
                            title="Register UCP Luxinity Roleplay",
                            components=[
                                ShortText(
                                    label="UCP Username",
                                    custom_id="username",
                                    placeholder="Masukkan username UCP kamu (contoh: Abielfrl)",
                                    required=True,
                                ),
                                ShortText(
                                    label="Password",
                                    custom_id="password",
                                    placeholder="Masukkan password UCP kamu",
                                    required=True,
                                ),
                            ],
                        )
                        await ctx.send_modal(modal=my_modal)  # send modal to users

                        # wait for user to enter the credentials
                        modal_ctx: ModalContext = await self.bot.wait_for_modal(
                            my_modal
                        )

                        # get channel to send the logs
                        w = self.bot.get_channel(966685759832723476)

                        # get modal responses
                        user = modal_ctx.responses["username"]
                        passwd = modal_ctx.responses["password"]

                        # hash passwords
                        hashed = bcrypt.hashpw(
                            passwd.encode("utf8"), bcrypt.gensalt()
                        ).decode("utf8")

                        # add records to database
                        sql = "INSERT INTO `playerucp` (`UCP`, `Password`, `discord_userid`) VALUES (%s, %s, %s)"
                        cursor.execute(
                            sql, (f"{user}", f"{hashed}", f"{ctx.author.id}")
                        )

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()

                        # send embed to ucp-logs
                        embed = Embed(title="New User Registered!", color=0x00FF00)
                        embed.add_field(name="Username:", value=user, inline=True)
                        embed.add_field(
                            name="Hashed Password:", value=f"||{hashed}||", inline=False
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

                        # add ucp registered role to user
                        ping_id = 971802984218517514
                        await ctx.author.add_role(
                            ping_id,
                            f"{user} just Registered, giving them the UCP role..",
                        )

                        # send username & password to user for safekeeping
                        manusya = Embed(
                            description="**Your New UCP Account**", color=0x17A168
                        )
                        manusya.add_field(
                            name="Username:", value=f"||{user}||", inline=True
                        )
                        manusya.add_field(
                            name="Password:", value=f"||{passwd}||", inline=False
                        )
                        try:
                            await ctx.author.send(embed=manusya)
                            await modal_ctx.send(
                                "Thank you for registering!\n\nCheck your DM's for your Username & Password!\nTo reset your password, please use `/change-password` commands.",
                                ephemeral=True,
                            )
                        except:
                            logging.info(f"Can't send message to {ctx.author} :(")
                            await modal_ctx.send(
                                "Thank you for registering!\n\nUnfortunately your server dm's are closed and we can't send your Username & Password\nTo reset your password, please use `/change-password` commands.",
                                ephemeral=True,
                            )
                        # send modal responses
                    else:
                        # send error message if user already registered
                        await ctx.send(
                            "You're already registered! (1 UCP account per discord user)\nIf you're having trouble, contact an admin.",
                            ephemeral=True,
                        )

        if ctx.custom_id == "user":
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
            )
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
                        modal_ctx: ModalContext = await self.bot.wait_for_modal(
                            my_modal
                        )

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
                        embed = Embed(title="UCP Username changed!", color=0x00FF00)
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
                        manusya.add_field(
                            name="Username:", value=f"{usern}", inline=False
                        )
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

        if ctx.custom_id == "password":
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
            )

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
                        modal_ctx: ModalContext = await self.bot.wait_for_modal(
                            my_modal
                        )

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
                        embed = Embed(title="UCP Password changed!", color=0x00FF00)
                        embed.add_field(
                            name="New Hashed Password:",
                            value=f"||{hashed}||",
                            inline=False,
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
    ready(bot)
