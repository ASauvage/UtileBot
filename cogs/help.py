import enum
import discord
import logging
from discord.ext import commands
from discord import app_commands
from main import UtileBot, VERSION_MAJOR, VERSION_MICRO, VERSION_MINOR, get_commands_list


HELP_COMMANDS = get_commands_list()
HELP_COMMANDS_ENUM = enum.Enum('HELP_COMMANDS_ENUMS', {x:x for x in HELP_COMMANDS})


class Help(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot
        self.commands_list = enum.Enum('commands', {command.name: command.name for command in self.bot.tree.walk_commands()})

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/help loaded")

    @commands.hybrid_command(name="help", with_app_command=True, description="A help command for commands")
    @app_commands.describe(command="(optional) The command name")
    async def help(self, ctx: commands.Context, command: HELP_COMMANDS_ENUM = None):
        embed = discord.Embed(title=self.bot.user,
                              description=f"`Prefix: {self.bot.settings['discord']['prefix']}`", color=0xE60012)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f"By {self.bot.developper.display_name}")

        if command:
            embed.add_field(name=command.value,
                            value=f"Description: {HELP_COMMANDS[command.value]['description']}\n"
                                  f"Parameters: {HELP_COMMANDS[command.value]['parameters']}"
                                  f"Default Permissions: {HELP_COMMANDS[command.value]['default_permissions']}"
                                  f"Guild Only: {HELP_COMMANDS[command.value]['guild_only']}"
                                  f"Extras: {HELP_COMMANDS[command.value]['extras'] if HELP_COMMANDS[command.value]['extras'] else 'No extra informations.'}",
                            inline=False)
        else:
            for command_name in HELP_COMMANDS:
                embed.add_field(name=command_name,
                                value=HELP_COMMANDS[command_name]["description"],
                                inline=False)

        await ctx.reply(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="version",with_app_command=True, description="Get informations of the bot")
    async def version(self, ctx: commands.Context):
        try:
            file = open(self.bot.path + "changelog.txt")
            content = file.read()
        except FileNotFoundError:
            content = "No changelog found"

        embed = discord.Embed(title="UtileBot", description="V{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_MICRO), color=0x221188)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f"https://github.com/ASauvage")

        embed.add_field(name="A utility bot for all your unnecessary needs",
                        value=f"Developed with Python 3 by {self.bot.developper.mention}",
                        inline=False)
        embed.add_field(name="Changelogs:",
                        value=content)

        await ctx.reply(embed=embed)


async def setup(bot: UtileBot):
    await bot.add_cog(Help(bot))