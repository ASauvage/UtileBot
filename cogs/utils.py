import discord
import logging
from discord.ext import commands
from discord import app_commands
from main import UtileBot
from common import encode_id, decode_id


class Utils(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/utils loaded")

    @commands.hybrid_command(name="private_message", with_app_command=True, description="Send an anonymous message to the server")
    @commands.dm_only()
    @app_commands.describe(title="The title of your message", message="Your anonymous message")
    async def private_message(self, ctx: commands.Context, title: str, message: str):
        embed = discord.Embed(title="Do you confirm your message?",
                              description="**{}**\n{}".format(title, message),
                              color=0x221188)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=encode_id(str(ctx.author.id)))

        view = YesCancelView()

        tmp = await ctx.reply(embed=embed, view=view)

        await view.wait()

        stats = "Cancel"
        if view.foo is None:
            await ctx.send("You took too long to respond")
            stats = "Timeout"
        elif view.foo is True:
            await self.bot.logchannel.create_thread(name=title, content=message)
            stats = "Yes"

        embed.set_footer(text="You selected: {}".format(stats))
        await tmp.edit(view=None, embed=embed)

    @commands.hybrid_command(name="private_message_reply", with_app_command=True, description="Reply to a topic anonymously")
    @commands.dm_only()
    @app_commands.describe(thread="The thread id", message="Your anonymous message")
    async def private_message_reply(self, ctx: commands.Context, thread: discord.Thread, message: str):
        embed = discord.Embed(title="Do you confirm your message?",
                              description="**{}**\n{}".format(thread.mention, message),
                              color=0x221188)
        embed.set_thumbnail(url=self.bot.user.avatar)

        view = YesCancelView()

        tmp = await ctx.reply(embed=embed, view=view)

        await view.wait()

        stats = "Cancel"
        if view.foo is None:
            await ctx.send("You took too long to respond")
            stats = "Timeout"
        elif view.foo is True:
            await thread.send(content=message)
            stats = "Yes"

        embed.set_footer(text="You selected: {}".format(stats))
        await tmp.edit(view=None, embed=embed)


class YesCancelView(discord.ui.View):
    foo : bool = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.foo = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.foo = False
        self.stop()


async def setup(bot: UtileBot):
    await bot.add_cog(Utils(bot))