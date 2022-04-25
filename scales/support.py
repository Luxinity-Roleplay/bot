from dis_snek import (
    message_command,
    Scale,
    Button,
    ButtonStyles,
    InteractionContext,
    AutoArchiveDuration,
    ChannelTypes,
    listen,
    slash_command,
    ActionRow,
    Permission,
    PermissionTypes,
)

thread_channel_id = 942417681703895100


class Support(Scale):
    @slash_command(
        "support-init",
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
    async def init(self, ctx: InteractionContext):
        components: list[ActionRow] = [
            ActionRow(
                Button(
                    style=ButtonStyles.SECONDARY,
                    label="Report Bug",
                    custom_id="create_bug_thread",
                    emoji="🐛",
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    label="Report Player",
                    custom_id="create_player_thread",
                    emoji="👨",
                ),
                Button(
                    style=ButtonStyles.DANGER,
                    label="Unban Request",
                    custom_id="create_unban_thread",
                    emoji="❓",
                ),
                Button(
                    style=ButtonStyles.GREEN,
                    label="Refund Request",
                    custom_id="create_refund_thread",
                    emoji="💰",
                ),
            )
        ]
        channel = await self.bot.fetch_channel(942754005333991444)
        await channel.send(
            "To get in touch with our staff, please choose your preferred help categories by pressing the button below.",
            components=components,
        )
        await ctx.send("Success", ephemeral=True)

    async def bug_thread(self, ctx: InteractionContext):
        channel = await self.bot.fetch_channel(thread_channel_id)

        thread = await channel.create_thread(
            name=f"{ctx.author.display_name}'s Bug Report thread",
            auto_archive_duration=AutoArchiveDuration.ONE_HOUR,
            reason="Bug Report Thread",
        )
        await thread.send(
            f"Hallow {ctx.author.mention}. Selamat datang di thread bug reportmu!\nTolong jelaskan masalah/bug yang kamu hadapi, dengan kriteria berikut:\n```md\nUCP :\nBug yang di temukan :\nBukti :\n```\nTeam kami akan membantumu segera."
        )
        await ctx.send(
            f"Thread Bug Report anda telah dibuat disini: {thread.mention}",
            ephemeral=True,
        )

    async def player_thread(self, ctx: InteractionContext):
        channel = await self.bot.fetch_channel(thread_channel_id)

        thread = await channel.create_thread(
            name=f"{ctx.author.display_name}'s Report Player thread",
            auto_archive_duration=AutoArchiveDuration.ONE_HOUR,
            reason="Report Player Thread",
        )
        await thread.send(
            f"Hallow {ctx.author.mention}. Selamat datang di thread report player mu!\nTolong jelaskan masalah yang kamu hadapi, dengan kriteria berikut:\n```md\nUCP :\nCharacter anda :\nCharacter pelaku :\nCeritakan apa yang terjadi :\nBukti :\n```\nTeam kami akan membantumu segera."
        )
        await ctx.send(
            f"Thread Report Player anda telah dibuat disini: {thread.mention}",
            ephemeral=True,
        )

    async def unban_thread(self, ctx: InteractionContext):
        channel = await self.bot.fetch_channel(thread_channel_id)

        thread = await channel.create_thread(
            name=f"{ctx.author.display_name}'s Unban Request thread",
            auto_archive_duration=AutoArchiveDuration.ONE_HOUR,
            reason="Unban Request Thread",
        )
        await thread.send(
            f"Hallow {ctx.author.mention}. Selamat datang di thread unban request mu!\nTolong jelaskan masalah yang kamu hadapi, dengan kriteria berikut:\n```md\nUCP :\nCharacter :\nAdmin yang bersangkutan (admin yang ban kamu) :\nAlasan kenapa bisa terkena ban :\nPermohonan unban :\nBukti :```\nTeam kami akan membantumu segera."
        )
        await ctx.send(
            f"Thread Unban Report anda telah dibuat disini: {thread.mention}",
            ephemeral=True,
        )

    async def refund_thread(self, ctx: InteractionContext):
        channel = await self.bot.fetch_channel(thread_channel_id)

        thread = await channel.create_thread(
            name=f"{ctx.author.display_name}'s Refund Request thread",
            auto_archive_duration=AutoArchiveDuration.ONE_HOUR,
            reason="Refund Request Thread",
        )
        await thread.send(
            f"Hallow {ctx.author.mention}. Selamat datang di thread Refund request mu!\nTolong jelaskan masalah yang kamu hadapi, dengan kriteria berikut:\n```md\nUCP :\nCharacter :\nBarang yang ingin di refund :\nCeritakan apa yang terjadi :\nBukti :\n```\nTeam kami akan membantumu segera."
        )
        await ctx.send(
            f"Thread Refund Request anda telah dibuat disini: {thread.mention}",
            ephemeral=True,
        )

    @listen()
    async def on_button(self, b):
        ctx = b.context
        if ctx.custom_id == "create_bug_thread":
            await ctx.defer(ephemeral=True)
            await self.bug_thread(ctx)
        if ctx.custom_id == "create_player_thread":
            await ctx.defer(ephemeral=True)
            await self.player_thread(ctx)
        if ctx.custom_id == "create_unban_thread":
            await ctx.defer(ephemeral=True)
            await self.unban_thread(ctx)
        if ctx.custom_id == "create_refund_thread":
            await ctx.defer(ephemeral=True)
            await self.refund_thread(ctx)


def setup(bot):
    Support(bot)
