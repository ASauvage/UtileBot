import asyncio
import os
import discord
import logging
from discord.ext import commands
from discord import app_commands
from datetime import date
from common import get_settings


VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_MICRO = 0


class UtileBot(commands.Bot):
    def __init__(self):
        # Variable
        self.settings = get_settings()
        self.path = os.path.dirname(__file__) + "/"
        self.private_message_forum = None


        # Intents
        intents = discord.Intents.all()
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
                         application_id=self.settings['discord']['application_id'],
                         tree_cls=app_commands.CommandTree)

    async def on_ready(self):
        logging.info("Logged in as {0.user}".format(self))
        print("logged in as {0.user}".format(self))

        self.developper = await self.fetch_user(187529417176645632)
        self.welcome_channel = self.get_channel(self.settings['discord']['channel_configurations']['welcome_channel_id'])
        self.admin_log_channel = self.get_channel(self.settings['discord']['channel_configurations']['admin_log_channel_id'])
        self.private_message_forum = self.get_channel(self.settings['discord']['channel_configurations']['private_forum_id'])


        await self.change_presence(status=discord.Status.online)

    async def setup_hook(self):
        """load all Cogs inside "Cogs" folder"""
        logging.info("Loading cogs...")
        for filename in os.listdir(os.path.dirname(__file__) + "/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Error: Missing Required Argument // {error}", ephemeral=True)
            logging.info(f"Error: MissingRequiredArgument // {error}")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Error: Bad Argument // {error}", ephemeral=True)
            logging.info(f"Error: Bad Argument // {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"Error: Missing Permissions// {error}", ephemeral=True)
            logging.info(f"Error: Missing Permissions // {error}")
        elif isinstance(error, commands.ChannelNotReadable):
            await ctx.reply(f"Error: Channel Not Readable // {error}", ephemeral=True)
            logging.info(f"Error: Channel Not Readable // {error}")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(f"Sorry {ctx.author.mention}, but your not allowed to use this command in private message", ephemeral=True)
            logging.info(f"Error : No Private Message // {error}")
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(f"Sorry {ctx.author.mention}, but your not allowed to use this command in servers", ephemeral=True)
        else:
            logging.info(f"Error: Unknown // {error}")


async def main(bot: UtileBot, token):
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main(UtileBot(), get_settings()['discord']['token']))
