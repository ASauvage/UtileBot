import enum
import discord
import logging
from discord.ext import commands
from discord import app_commands
from main import UtileBot, extract_commands_data


class Owner(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
            logging.info(f"cogs/owner loaded")

    @commands.hybrid_command(name="sync", with_app_command=True, description="Sync commands with discord (Owner only)")
    async def sync(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            logging.info(f"command(s) syncronisation")
            try:
                synced = await self.bot.tree.sync()
                await ctx.reply(f"Synced {len(synced)} command(s)")
                logging.info(f"Synced {len(synced)} command(s)")
            except Exception as e:
                await ctx.reply(e.__str__())

    @commands.hybrid_command(name="extract_commands", with_app_command=True, description="Extract information from commands (Owner only)")
    async def extract_commands(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            extract_commands_data(self.bot.tree.walk_commands())

            await ctx.reply("Data extract", ephemeral=True)

    @commands.hybrid_command(name="find_user", with_app_command=True, description="Find a person's profile from their id")
    @app_commands.describe(user="The user id")
    async def find_user(self, ctx: commands.Context, user: discord.User):
        await ctx.reply(user.mention)


async def setup(bot: UtileBot):
    await bot.add_cog(Owner(bot))