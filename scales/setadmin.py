from dis_snek import (
    slash_command,
    slash_option,
    OptionTypes,
    SlashCommandChoice,
    Permission,
    PermissionTypes,
    Scale,
    Embed
)
from typing import Optional

import datetime
import dis_snek


class setadmin(Scale):
    @slash_command(
        "set-admin",
        description="Set a player admin level",
        permissions=[
            Permission(
                id=846702912118063114,  # founder
                guild_id=812150001089118210,
                type=PermissionTypes.ROLE,
                permission=True,
            ),
            Permission(
                id=966679659733479544,  # developer
                guild_id=812150001089118210,
                type=PermissionTypes.ROLE,
                permission=True,
            ),
            Permission(
                id=851290742038200391,  # management
                guild_id=812150001089118210,
                type=PermissionTypes.ROLE,
                permission=True,
            ),
            Permission(
                id=812150001089118210,  # denied @everyone role
                guild_id=812150001089118210,
                type=PermissionTypes.ROLE,
                permission=False,
            ),
        ],
    )
    @slash_option(
        name="member",
        description="The target @member",
        required=True,
        opt_type=OptionTypes.USER,
    )
    @slash_option(
        name="level",
        description="Admin level you want to promote",
        required=True,
        opt_type=OptionTypes.INTEGER,
        choices=[
            SlashCommandChoice(name="Player", value=0),
            SlashCommandChoice(name="Junior Helper", value=1),
            SlashCommandChoice(name="Senior Helper", value=2),
            SlashCommandChoice(name="Admin Level 1", value=3),
            SlashCommandChoice(name="Admin Level 2", value=4),
            SlashCommandChoice(name="Admin Level 3", value=5),
            SlashCommandChoice(name="Management (setara founder)", value=6),
            SlashCommandChoice(name="Founder", value=7),
        ],
    )
    @slash_option(
        "reason",
        "The reason of promote/demote",
        OptionTypes.STRING,
        required=False,
    )
    async def set_admin(
        self,
        ctx,
        member: dis_snek.Member,
        level: int,
        reason: Optional[str] = "No reason provided",
    ):
        # check if user has role same with the author and/or higher role than the target

        if ctx.author.top_role == member.top_role:
            embed = Embed(
                description=f":x: You can't promote/demote with the same role as you!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if ctx.author.top_role.position < member.top_role.position:
            embed = Embed(
                description=f":x: You can't promote/demote with roles higher than yours!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # ping the mysql server
        connection.ping(reconnect=True)

        with connection:
            with connection.cursor() as cursor:
                # check if user is already registered
                sql = f"SELECT `discord_userid` FROM `playerucp` WHERE `discord_userid`=%s"
                cursor.execute(sql, (member.id))
                result = cursor.fetchone()

                if result is not None:
                    # get channel to send the logs
                    w = self.bot.get_channel(966685759832723476)

                    # update records to database
                    sql = "UPDATE `playerucp` SET `Admin` = %s WHERE `playerucp`.`discord_userid` = %s"
                    cursor.execute(sql, (level, f"{member.id}"))

                    # connection is not autocommit by default. So you must commit to save
                    # your changes.
                    connection.commit()

                    # add level checks
                    if level == 0:
                        rank = "Player"
                    if level == 1:
                        rank = "Junior Helper"
                    if level == 2:
                        rank = "Senior Helper"
                    if level == 3:
                        rank = "Admin Level 1"
                    if level == 4:
                        rank = "Admin Level 2"
                    if level == 5:
                        rank = "Admin Level 3"
                    if level == 6:
                        rank = "Management"
                    if level == 7:
                        rank = "Founder"

                    # send embed to ucp-logs
                    embed = dis_snek.Embed(
                        title="User Promoted/Demoted", color=0x00FF00
                    )
                    embed.add_field(name="New Rank:", value=rank, inline=True)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.set_author(
                        name=f"{member.username}#{member.discriminator}",
                        url=f"https://discordapp.com/users/{member.id}",
                        icon_url=member.avatar.url,
                    )
                    embed.set_thumbnail(url=ctx.author.avatar.url)
                    embed.set_footer(
                        text=f"{ctx.guild.name} | User ID: {ctx.author.id}",
                        icon_url=ctx.guild.icon.url,
                    )
                    embed.timestamp = datetime.datetime.utcnow()
                    await w.send(embed=embed)

                    # notify user the changes
                    try:
                        await member.send(
                            f"You have been promoted/demoted to `{rank}` by {ctx.author.mention}\nReason: {reason}"
                        )
                        await ctx.send(
                            f"Successfully promoted/demoted {member.mention}\n\nI already notified the user about the changes.",
                            ephemeral=True,
                        )
                    except:
                        logging.info(f"Can't send message to {ctx.author} :(")
                        await ctx.send(
                            f"Successfully promoted/demoted {member.mention}\n\nUnfortunately i can't notify the user about the changes because their server dm's are closed :(",
                            ephemeral=True,
                        )
                else:
                    # send error message if user already registered
                    await ctx.send(
                        "Invalid user!",
                        ephemeral=True,
                    )


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    setadmin(bot)