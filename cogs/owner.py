import discord
import logging
from discord.ext import commands
from main import UtileBot


class Owner(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
            logging.info(f"cogs/owner loaded")

    @commands.command()
    async def sync(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            logging.info(f"command(s) syncronisation")
            try:
                synced = await self.bot.tree.sync()
                await ctx.channel.send(f"Synced {len(synced)} command(s)")
                logging.info(f"Synced {len(synced)} command(s)")
            except Exception as e:
                await ctx.channel.send(e.__str__())

    @commands.command()
    async def find_user(self, ctx: commands.Context, user_id: int):
        await ctx.send(f'<@{user_id}>')


async def setup(bot: UtileBot):
    await bot.add_cog(Owner(bot))