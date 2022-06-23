# Credits to Discord-Snake-Pit/Dis-secretary

from naff.models import Extension, GuildNews, Message, listen


class announce(Extension):
    @listen()
    async def on_message_create(self, event):
        message: Message = event.message
        if isinstance(message.channel, GuildNews):
            try:
                await message.publish()
            except Exception:
                print("publish failed")
                pass
            else:
                print("publish succeeded")


def setup(bot):
    announce(bot)
