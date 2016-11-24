import pysmash
from .utils import config, checks
from discord.ext import commands

smash = pysmash.SmashGG()


class Smashy:
    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('smashy.json', loop=bot.loop)

    # TODo write the help commands
    @commands.group(pass_context=True, no_pm=True)
    async def smashy(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @commands.group(pass_context=True, no_pm=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @add.command(name='tournament')
    @checks.admin_or_permissions()
    async def add_tournament(self, *tournament_names: str):
        for tournament_name in tournament_names:
            await self.add_specific(tournament_name, 'tournament_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='event')
    @checks.admin_or_permissions()
    async def add_event(self, *event_names: str):
        for event_name in event_names:
            await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='bracket')
    @checks.admin_or_permissions()
    async def add_bracket(self, *bracket_ids: str):
        for bracket_id in bracket_ids:
            await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='set')
    @checks.admin_or_permissions()
    async def add_set(self, *set_ids: str):
        for set_id in set_ids:
            await self.add_specific(set_id, 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def add_displayed_set(self, *displayed_set_ids: str):
        for displayed_set_id in displayed_set_ids:
            await self.add_specific(displayed_set_id, 'set_ids')
            await self.add_specific(displayed_set_id, 'displayed_set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific(self, specific: str, specific_db_key: str):
        specifics = self.config.get(specific_db_key, [])
        if specific in specifics:
            return
        specifics.append(specific)
        await self.config.put(specific_db_key, specifics)

    @commands.group(pass_context=True, no_pm=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @remove.command(name='tournament')
    @checks.admin_or_permissions()
    async def remove_tournament(self, *specific_tournament_names: str):
        tournament_names = self.config.get('tournament_names', [])
        for specific_tournament_name in specific_tournament_names:
            if specific_tournament_name in tournament_names:
                try:
                    tournament_names.remove(specific_tournament_name)
                except ValueError:
                    pass

            await self.config.put('tournament_names', tournament_names)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='event')
    @checks.admin_or_permissions()
    async def remove_event(self, *specific_event_names: str):
            event_names = self.config.get('event_names', [])
            for specific_event_name in specific_event_names:
                if specific_event_name in event_names:
                    try:
                        event_names.remove(specific_event_name)
                    except ValueError:
                        pass
                await self.config.put('event_names', event_names)
            await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='bracket')
    @checks.admin_or_permissions()
    async def remove_bracket(self, *specific_bracket_ids: str):
        bracket_ids = self.config.get('bracket_ids', [])
        for specific_bracket_id in specific_bracket_ids:
            if specific_bracket_id in bracket_ids:
                try:
                    bracket_ids.remove(specific_bracket_id)
                except ValueError:
                    pass
            await self.config.put('bracket_ids', bracket_ids)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def remove_displayed_set(self, *displayed_set_id: str):
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        if displayed_set_id in displayed_set_ids:
            try:
                displayed_set_ids.remove(displayed_set_id)
            except ValueError:
                pass
        await self.config.put('displayed_set_ids', displayed_set_ids)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='set', pass_context=True)
    @checks.admin_or_permissions()
    async def remove_set(self, ctx, *set_id: str):
        set_ids = self.config.get('set_ids', [])
        if set_id in set_ids:
            try:
                set_ids.remove(set_id)
            except ValueError:
                pass
        await self.config.put('set_ids', set_ids)
        await ctx.invoke(self.remove_displayed_set, *set_id)

    @remove.group(name='all', invoke_without_command=True)
    @checks.is_owner()
    async def remove_all(self):
        # I know this is ugly but list.remove(list_id) didn't work properly for some reason
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        for i in range(len(displayed_set_ids)):
            del displayed_set_ids[0]
            await self.config.put('displayed_set_ids', displayed_set_ids)

        set_ids = self.config.get('set_ids', [])
        for i in range(len(set_ids)):
            del set_ids[0]
            await self.config.put('set_ids', set_ids)

        event_names = self.config.get('event_names', [])
        for i in range(len(event_names)):
            del event_names[0]
            await self.config.put('event_names', event_names)

        tournament_names = self.config.get('tournament_names', [])
        for i in range(len(tournament_names)):
            del tournament_names[0]
            await self.config.put('tournament_names', tournament_names)

        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='displayed_sets')
    @checks.is_owner()
    async def remove_all_displayed_sets(self):
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        for i in range(len(displayed_set_ids)):
            del displayed_set_ids[0]
            await self.config.put('displayed_set_ids', displayed_set_ids)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='sets')
    @checks.is_owner()
    async def remove_all_sets(self):
        set_ids = self.config.get('set_ids', [])
        for i in range(len(set_ids)):
            del set_ids[0]
            await self.config.put('set_ids', set_ids)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='events')
    @checks.is_owner()
    async def remove_all_events(self):
        event_names = self.config.get('event_names', [])
        for i in range(len(event_names)):
            del event_names[0]
            await self.config.put('event_names', event_names)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='tournaments')
    @checks.is_owner()
    async def remove_all_tournaments(self):
        tournament_names = self.config.get('tournament_names', [])
        for i in range(len(tournament_names)):
            del tournament_names[0]
            await self.config.put('tournament_names', tournament_names)
        await self.bot.say('\N{OK HAND SIGN}')

    @commands.group(pass_context=True, no_pm=True)
    async def get(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @get.group(name='events', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_events(self):
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            event_names = smash.tournament_show_events(tournament_name)
            for event_name in event_names['events']:
                await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_events.group(name='tournament')
    @checks.admin_or_permissions()
    async def get_events_tournament(self, *tournament_names: str):
        for tournament_name in tournament_names:
            event_names = smash.tournament_show_events(tournament_name)
            for event_name in event_names['events']:
                await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @get.group(name='brackets', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_brackets(self):
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_brackets.command(name='tournament')
    @checks.admin_or_permissions()
    async def get_brackets(self, *tournament_names: str):
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_brackets.command(name='event')
    @checks.admin_or_permissions()
    async def get_brackets(self, *event_names: str):
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            for event_name in event_names:
                brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get.group(name='sets', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_sets(self):
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            print(tournament_name)
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                sets = smash.tournament_show_sets(tournament_name, event_name)
                print(sets)
                for specific_set in sets:
                    print(specific_set['id'])
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('tournament')
    @checks.admin_or_permissions()
    async def get_sets_tournament(self, *tournament_names: str):
        for tournament_name in tournament_names:
            events = smash.tournament_show_events(tournament_name)
            for event_name in events['events']:
                sets = smash.tournament_show_sets(tournament_name, event_name)
                for specific_set in sets:
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('event')
    @checks.admin_or_permissions()
    async def get_sets_event(self, *event_names: str):
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            for event_name in event_names:
                sets = smash.tournament_show_sets(tournament_name, event_name)
                for specific_set in sets:
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('bracket')
    @checks.admin_or_permissions()
    async def get_sets_bracket(self, *bracket_ids: str):
        for bracket_id in bracket_ids:
            sets = smash.bracket_show_sets(bracket_id)
            for specific_set in sets:
                await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @smashy.command(name='test', pass_context=True)
    @checks.admin_or_permissions()
    async def smashy_test(self, ctx):
        test = smash.tournament_show_events('lunox-api-test')
        print(test)
        await self.bot.say('test successful')

        # TODO add setup command
        # TODO add matchups command


def setup(bot):
    bot.add_cog(Smashy(bot))
