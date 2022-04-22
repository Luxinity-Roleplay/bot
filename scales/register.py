from dis_snek import (
    slash_command,
    Modal,
    ShortText,
    cooldown,
    Buckets,
    Scale,
)
from dotenv import load_dotenv

import os
import bcrypt
import pymysql.cursors
import datetime
import dis_snek

load_dotenv()

# Connect to the database
connection = pymysql.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME"),
    cursorclass=pymysql.cursors.DictCursor,
)


class register(Scale):
    @slash_command(
        "register", description="Register akun UCP (Max. 1 akun per discord user!)"
    )
    async def register(self, ctx):
        connection.ping(reconnect=True)
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
        await ctx.send_modal(modal=my_modal)  # send modal to

        modal_ctx: ModalContext = await self.bot.wait_for_modal(
            my_modal
        )  # wait for user to enter the credentials

        w = self.bot.get_channel(966685759832723476)  # get channel to send the logs

        # get modal responses
        user = modal_ctx.responses["username"]
        passwd = modal_ctx.responses["password"]

        # send username & password to user for safekeeping
        embed = dis_snek.Embed(description="**Your New UCP Account**", color=0x00FF00)
        embed.add_field(name="Username:", value=f"||{user}||", inline=True)
        embed.add_field(name="Password:", value=f"||{passwd}||", inline=False)
        await ctx.author.send(embed=embed)

        # log new ucp account to database
        with connection:
            with connection.cursor() as cursor:
                sql = f"SELECT `discord_userid` FROM `playerucp` WHERE `discord_userid`=%s"
                cursor.execute(sql, (ctx.author.id))
                result = cursor.fetchone()
                print(result)

                if result is None:
                    # hash passwords
                    hashed = bcrypt.hashpw(
                        passwd.encode("utf8"), bcrypt.gensalt()
                    ).decode("utf8")

                    # add records to database
                    sql = "INSERT INTO `playerucp` (`UCP`, `Password`, `discord_userid`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (f"{user}", f"{hashed}", f"{ctx.author.id}"))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()

                    # send embed to ucp-logs
                    embed = dis_snek.Embed(title="New User Registered!", color=0x00FF00)
                    embed.add_field(name="Username:", value=user, inline=True)
                    # embed.add_field(
                    #    name="Password:", value=f"||{passwd}||", inline=False
                    # )
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

                    # send modal responses
                    await modal_ctx.send(
                        "Thank you for registering!\n\nCheck your DM's for your Username & Password!",
                        ephemeral=True,
                    )
                else:
                    # send error message if user already registered
                    await modal_ctx.send(
                        "You're already registered! (1 UCP account per discord user)\nIf you're having trouble, contact an admin.",
                        ephemeral=True,
                    )


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    register(bot)
