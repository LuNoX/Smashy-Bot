import pysmash
from .utils import config, checks
from discord.ext import commands

smash = pysmash.SmashGG()
default_tournament = 'lunox-api-test'

class Smashy:

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('smashy.json', loop=bot.loop)

    @commands.group(pass_context=True, no_pm=True)
    async def smashy (self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))



def setup(bot):
    bot.add_cog(Smashy(bot))