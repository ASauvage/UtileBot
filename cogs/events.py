import logging
import discord
from discord.ext import commands
from main import UtileBot


class Events(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/events loaded")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(title="Welcume :saluting_face:",
                              description=member.mention,
                              color=0x221188)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="We are now {}".format(self.bot.welcome_channel.guild.member_count))

        await self.bot.welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(title="Goodbye :saluting_face:",
                              description=member.mention,
                              color=0x221188)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="We are now {}".format(self.bot.welcome_channel.guild.member_count))

        await self.bot.welcome_channel.send(embed=embed)


async def setup(bot: UtileBot):
    await bot.add_cog(Events(bot))
