import enum
import discord
import logging
from discord.ext import commands
from discord import app_commands
from main import UtileBot, VERSION_MAJOR, VERSION_MICRO, VERSION_MINOR
from common import get_commands_list


class Help(commands.Cog):
    help_commands: dict = get_commands_list()
    help_commands_enums : enum.Enum = enum.Enum('HELP_COMMANDS_ENUMS', {x:x for x in help_commands})

    def __init__(self, bot: UtileBot):
        self.bot = bot
        self.commands_list = enum.Enum('commands', {command.name: command.name for command in self.bot.tree.walk_commands()})

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/help loaded")

    @commands.hybrid_command(name="help", with_app_command=True, description="A help command for commands")
    @app_commands.describe(command="(optional) The command name")
    async def help(self, ctx: commands.Context, command: help_commands_enums = None):
        embed = discord.Embed(title=self.bot.user,
                              description=f"`Bot Prefix: {self.bot.settings['discord']['prefix']}`", color=0xE60012)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f"By {self.bot.developper.display_name}")

        if command:
            embed.add_field(name=command.value,
                            value="__Description__: {}\n__Parameter(s)__:\n- {}\n__Guild Only__: {}\n__Extras__: {}".format(
                                self.help_commands[command.value]['description'],
                               '\n- '.join(self.help_commands[command.value]['parameters']) if self.help_commands[command.value]['parameters'] else 'No parameter',
                               self.help_commands[command.value]['guild_only'],
                               self.help_commands[command.value]['extras'] if self.help_commands[command.value]['extras'] else 'No extra informations.'
                            ),
                            inline=False)
        else:
            for command_name in self.help_commands:
                embed.add_field(name=command_name,
                                value=self.help_commands[command_name]["description"],
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