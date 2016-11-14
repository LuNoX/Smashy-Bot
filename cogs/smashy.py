import pysmash
from .utils import config, checks
from discord.ext import commands

smash = pysmash.SmashGG()


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
    @checks.admin_or_permissions()
    async def smashy_test(self, ctx):
        test = smash.tournament_show('lunox-api-test')
        print(test)
        await self.bot.say('test successful')

    @add.command(name='tournament')
    @checks.admin_or_permissions()
    async def add_tournament(self, *, tournament_name: str):
        tournament_names = self.config.get('tournament_name', [])

        if tournament_name in tournament_names:
            await self.bot.say('Tournament already exists')
            return

        tournament_names.append(tournament_name)
        await self.config.put('tournament_names', tournament_names)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='tournament')
    @checks.admin_or_permissions()
    async def remove_tournament(self, *, tournament_name: str):
        self.remove_specific_tournament(tournament_name)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_tournament(self, tournament_name):
        tournament_names = self.config.get('tournament_names', [])
        if tournament_name in tournament_names:
            try:
                tournament_names.remove(tournament_name)
            except ValueError:
                pass

        await self.config.put('tournament_names', tournament_names)

    @get.group(name='events', pass_context=True, invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_events(self):
        tournament_names = self.config.get('tournament_names', [])
        print(tournament_names)
        for tournament_name in tournament_names:
            print(tournament_name)
            return # remove this once the following function is implemented in pysmash
            # noinspection PyUnreachableCode
            events = smash.tournament_show_events(tournament_name)

            for event_id in events['event_ids']:
                print(event_id)
                await self.add_specific_event(event_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='event')
    @checks.admin_or_permissions()
    async def add_event(self, *, event_id: str):
        event_ids = self.config.get('event_ids', [])

        if event_id in event_ids:
            await self.bot.say('Event already exists')
            return

        event_ids.append(event_id)
        await self.config.put('event_ids', event_ids)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_event(self, event_id: str):
        event_ids = self.config.get('event_ids', [])
        if event_id in event_ids:
            return

        event_ids.append(event_id)
        await self.config.put('event_ids', event_ids)

    @remove.command(name='event')
    @checks.admin_or_permissions()
    async def remove_event(self, *, event_id: str):
        self.remove_specific_event(event_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_event(self, event_id):
        event_ids = self.config.get('event_ids', [])
        if event_id in event_ids:
            try:
                event_ids.remove(event_id)
            except ValueError:
                pass

        await self.config.put('event_ids', event_ids)

    @get.group(name='sets', pass_context=True, invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_sets(self):
        tournament_names = self.config.get('tournament_names', [])
        print(tournament_names)
        for tournament_name in tournament_names:
            print(tournament_name)
        # replace all of this once show_tournament_sets works
        # replace this with show_tournament_events['bracket_names'] once the function is implemented in pysmash
            bracket_names = ['rivals-of-aether-singles', 'melee-singles']  # 'wii-u-singles'] KeyError needs to be fixed
            for bracket_name in bracket_names:
                # print('bracket name: {}'.format(bracket_name))
                brackets = smash.tournament_show_with_brackets(tournament_name, '', bracket_name)
                # print('bracket: {}'.format(brackets))
                for bracket in brackets['bracket_ids']:
                    # print('bracket id: {}'.format(bracket))
                    sets = smash.bracket_show_sets(bracket)
                    for single_set in sets:
                        await self.add_specific_set('set_ids', single_set['id'])
                        # print('sets: {}'.format(sets))
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='set')
    @checks.admin_or_permissions()
    async def add_set(self, *, set_id: str):
        await self.add_specific_set('set_ids', set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def add_displayed_set(self, *, set_id: str):
        await self.add_specific_set('set_ids', set_id)
        await self.add_specific_set('displayed_set_ids', set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_set(self, set_key_name: str, set_id: str):
        set_ids = self.config.get(set_key_name, [])
        if set_id in set_ids:
            return

        set_ids.append(set_id)
        await self.config.put(set_key_name, set_ids)

    @remove.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def remove_displayed_set(self, *, displayed_set_id: str):
        await self.remove_specific_set('displayed_set_ids', displayed_set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='set')
    @checks.admin_or_permissions()
    async def remove_set(self, *, set_id: str):
        await self.remove_specific_set('set_ids', set_id)
        await self.remove_specific_set('displayed_set_ids', set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_set(self, set_key_name: str, set_id: str):
        set_ids = self.config.get(set_key_name, [])

        if set_id in set_ids:
            try:
                set_ids.remove(set_id)
            except ValueError:
                print('value error')
                pass
        await self.config.put(set_key_name, set_ids)

    @remove.group(name='all', invoke_without_command=True)
    @checks.is_owner()
    async def remove_all(self):
        # I know this is ugly but list.remove(list_id) didn't work properly for some reason
        set_ids = self.config.get('set_ids', [])
        for i in range(len(set_ids)):
            del set_ids[0]
            await self.config.put('set_ids', set_ids)

        displayed_set_ids = self.config.get('displayed_set_ids', [])
        for i in range(len(displayed_set_ids)):
            del displayed_set_ids[0]
            await self.config.put('displayed_set_ids', displayed_set_ids)

        event_ids = self.config.get('event_ids', [])
        for i in range(len(event_ids)):
            del event_ids[0]
            await self.config.put('event_ids', event_ids)

        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='sets')
    @checks.is_owner()
    async def remove_all_sets(self):
        set_ids = self.config.get('set_ids', [])
        for i in range(len(set_ids)):
            del set_ids[0]
            await self.config.put('set_ids', set_ids)

    @remove_all.command(name='displayed_sets')
    @checks.is_owner()
    async def remove_all_displayed_sets(self):
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        for i in range(len(displayed_set_ids)):
            del displayed_set_ids[0]
            await self.config.put('displayed_set_ids', displayed_set_ids)

    @remove_all.command(name='events')
    @checks.is_owner()
    async def remove_all_events(self):
        event_ids = self.config.get('event_ids', [])
        for i in range(len(event_ids)):
            del event_ids[0]
            await self.config.put('event_ids', event_ids)

    @remove_all.command(name='tournaments')
    @checks.is_owner()
    async def remove_all_tournaments(self):
        tournament_names = self.config.get('tournament_names', [])
        for i in range(len(tournament_names)):
            del tournament_names[0]
            await self.config.put('tournament_names', tournament_names)


def setup(bot):
    bot.add_cog(Smashy(bot))
