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
    async def smashy(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @commands.group(pass_context=True, no_pm=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @commands.group(pass_context=True, no_pm=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @commands.group(pass_context=True, no_pm=True)
    async def get(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @smashy.command(name='test', pass_context=True)
    @checks.admin_or_permissions(manage_channels=True)
    async def smashy_test(self, ctx):
        tournaments = smash.tournament_show(default_tournament)
        print(tournaments)
        brackets = smash.tournament_show_with_brackets(default_tournament, '', 'rivals-of-aether-singles')
        print(brackets)
        sets = smash.bracket_show_sets(brackets['bracket_ids'][0])
        print(sets[0])
        await self.bot.say(tournaments)
        await self.bot.say('test successful')

    @add.command(name='Event')
    @checks.admin_or_permissions(manage_channels=True)
    async def add_event(self, *, event_id: int):
        event_ids = self.config.get('event_ids', [])

        if event_id in event_ids:
            await self.bot.say('Event already exists')
            return

        event_ids.append(event_id)
        await self.config.put('event_ids', event_ids)
        await self.bot.say('\U0001f44c')

    @remove.command(name='Event')
    @checks.admin_or_permissions(manage_channels=True)
    async def remove_event(self, *, event_id: int):
        event_ids = self.config.get('event_ids', [])

        if event_id in event_ids:
            try:
                event_ids.remove(event_id)
            except ValueError:
                pass

        await self.config.put('event_ids', event_ids)
        await self.bot.say('\U0001f44c')

    @add.command(name='Set')
    @checks.admin_or_permissions(manage_channels=True)
    async def add_set(self, *, set_id: int):
        await self.add_sepcific_set('set_ids', set_id)
        await self.bot.say('\U0001f44c')

    @add.command(name='displayedSet')
    @checks.admin_or_permissions(manage_channels=True)
    async def add__displayed_set(self, *, set_id: int):
        await self.add_sepcific_set('set_ids', set_id)
        await self.add_sepcific_set('displayed_set_ids', set_id)
        await self.bot.say('\U0001f44c')

    async def add_sepcific_set(self, set_key_name: str, set_id: int):
        set_ids = self.config.get(set_key_name, [])
        if set_id in set_ids:
            return

        set_ids.append(set_id)
        await self.config.put(set_key_name, set_ids)

    @remove.command(name='DisplayedSet')
    @checks.admin_or_permissions(manage_channels=True)
    async def remove_displayed_set(self, *, displayed_set_id: int):
        await self.remove_specific_set('displayed_set_ids', displayed_set_id)
        await self.bot.say('\U0001f44c')

    @remove.command(name='Set')
    @checks.admin_or_permissions(manage_channels=True)
    async def remove_set(self, *, set_id: int):
        await self.remove_specific_set('set_ids', set_id)
        await self.remove_specific_set('displayed_set_ids', set_id)
        await self.bot.say('\U0001f44c')

    async def remove_specific_set(self, set_key_name: str, set_id: int):
        set_ids = self.config.get(set_key_name, [])

        if set_id in set_ids:
            try:
                set_ids.remove(set_id)
            except ValueError:
                pass
        await self.config.put(set_key_name, set_ids)


def setup(bot):
    bot.add_cog(Smashy(bot))
