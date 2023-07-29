import asyncio
import json
import os
import discord
import logging
from discord.ext import commands
from datetime import date


VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_MICRO = 0


class UtileBot(commands.Bot):
    def __init__(self):
        # Variable
        self.settings = get_settings()
        self.path = os.path.dirname(__file__) + "/"
        self.logchannel = None


        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.dm_messages = True
        intents.reactions = True

        # Logging
        try:
            os.path.join(self.path, "logs")
        except FileExistsError:
            pass

        logging.basicConfig(filename=f"./logs/{date.today()}.log",
                            level=logging.INFO,
                            format="%(asctime)s [%(levelname)s] %(message)s")

        super().__init__(command_prefix=self.settings['discord']['prefix'],
                         help_command=None,
                         intents=intents,
                         application_id=self.settings['discord']['application_id'])

    async def on_ready(self):
        logging.info("Logged in as {0.user}".format(self))
        print("logged in as {0.user}".format(self))
        self.logchannel = self.get_channel(self.settings['discord']['log_channel_id'])

        await self.change_presence(status=discord.Status.online)

    async def setup_hook(self):
        """load all Cogs inside "Cogs" folder"""
        logging.info("Loading cogs...")
        for filename in os.listdir(os.path.dirname(__file__) + "/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f"Error: Missing Required Argument // {error}")
            await ctx.message.delete()
            logging.info(f"Error: MissingRequiredArgument // {error}")
        elif isinstance(error, commands.BadArgument):
            await ctx.channel.send(f"Error: Bad Argument // {error}")
            await ctx.message.delete()
            logging.info(f"Error: Bad Argument // {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"Error: Missing Permissions// {error}")
            await ctx.message.delete()
            logging.info(f"Error: Missing Permissions // {error}")
        elif isinstance(error, commands.ChannelNotReadable):
            await ctx.channel.send(f"Error: Channel Not Readable // {error}")
            await ctx.message.delete()
            logging.info(f"Error: Channel Not Readable // {error}")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.channel.send(
                f"Sorry {ctx.author.mention}, but your not allowed to use this command in private message")
            logging.info(f"Error : No Private Message // {error}")
        else:
            logging.info(f"Error: Unknown // {error}")

    async def close(self):
        await super().close()


def get_settings():
    with open(os.path.dirname(__file__) + '/settings.json', 'r') as json_file:
        return json.load(json_file)


async def main(bot: UtileBot, token):
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main(UtileBot(), get_settings()['discord']['token']))
