import discord
import logging
from base64 import b64encode, b64decode
from discord.ext import commands
from discord import app_commands
from main import UtileBot
from random import sample


class Utils(commands.Cog):
    def __init__(self, bot: UtileBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"cogs/utils loaded")

    @app_commands.command(name="private")
    async def private(self, interaction: discord.Interaction, message: str):
        embed = discord.Embed(title="Do you confirm your message?", description=message, color=0x221188)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=encode_id(str(interaction.user.id)))

        await interaction.response.send_message(embed=embed)


def encode_id(id: str) -> str:
    id_list = [id[i:i+3] for i in range(0, len(id), 3)]
    pattern = sample(range(0, 6), 6)

    hashed_id = ''.join([id_list[pattern.index(x)] for x in range(0, 6)])

    hashed_id += ''.join(str(e) for e in pattern)

    return b64encode(hashed_id.encode()).decode()


def decode_id(hashed_id: str) -> str:
    blend_id = b64decode(hashed_id).decode()
    id_list = [blend_id[i:i + 3] for i in range(0, len(blend_id) - 6, 3)]
    pattern = [int(blend_id[i:i + 1]) for i in range(len(blend_id) - 6, len(blend_id), 1)]

    id = [id_list[x] for x in pattern]

    return ''.join(id)


async def setup(bot: UtileBot):
    await bot.add_cog(Utils(bot))