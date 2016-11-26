from .utils import config, checks
from discord.ext import commands

class Aethernet:

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Aethernet(bot))