import enum
import discord
import logging
from discord.ext import commands
from discord import app_commands
from main import UtileBot, VERSION_MAJOR, VERSION_MICRO, VERSION_MINOR, get_settings


HELP_COMMANDS = enum.Enum('HELP_COMMANDS', {x:x for x in get_settings()['discord']['help']})


class Help(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/help loaded")

    @app_commands.command(name="help", description="")
    async def help(self, interaction: discord.Interaction, command: HELP_COMMANDS):
        embed = discord.Embed(title=self.bot.user,
                              description="\n\n", color=0xE60012)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text='By <@187529417176645632>')

        if command:
            embed.add_field(name=self.bot.settings['discord']['prefix'] + self.bot.settings['discord']['help'][command]['title'],
                            value=self.bot.settings['discord']['help'][command]['description'], inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            for command_name in self.bot.settings['discord']['help']:
                embed.add_field(name=self.bot.settings['discord']['prefix'] + self.bot.settings['discord']['help'][command_name]['title'],
                                value=self.bot.settings['discord']['help'][command_name]["description"], inline=False)

            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="version", description="")
    async def version(self, interaction: discord.Interaction):
        try:
            file = open(self.bot.path + "changelog.txt")
            content = file.read()
        except FileNotFoundError:
            content = "No changelog found"

        embed = discord.Embed(title="UtileBot", description="V{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_MICRO), color=0x221188)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text="By <@187529417176645632>")

        embed.add_field(name="A utility bot for all your unnecessary needs",
                        value="Developed with Python3",
                        inline=False)
        embed.add_field(name="Changelogs:",
                        value=content)

        await interaction.response.send_message(embed=embed)


async def setup(bot: UtileBot):
    await bot.add_cog(Help(bot))