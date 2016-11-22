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
        test = smash.tournament_show_events('lunox-api-test')
        print(test)
        await self.bot.say('test successful')

    @add.command(name='tournament')
    @checks.admin_or_permissions()
    async def add_tournament(self, *, tournament_names: str):
        tournament_names = tournament_names.split(" ")
        for tournament_name in tournament_names:
            await self.add_specific_tournament(tournament_name)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_tournament(self, tournament_name: str):
        tournament_names = self.config.get('tournament_names', [])
        if tournament_name in tournament_names:
            return
        tournament_names.append(tournament_name)
        await self.config.put('tournament_names', tournament_names)

    # TODO remove remove_specific funcs
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

    @get.group(name='events', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_events(self, *, tournament_names: str = None):
        if tournament_names is None:
            tournament_names = self.config.get('tournament_names', [])
        else:
            tournament_names = tournament_names.split(" ")
        for tournament_name in tournament_names:
            event_names = smash.tournament_show_events(tournament_name)
            for event_name in event_names['events']:
                await self.add_specific_event(event_name)
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='event')
    @checks.admin_or_permissions()
    async def add_event(self, *, event_names: str):
        event_names = event_names.split(" ")
        for event_name in event_names:
            await self.add_specific_event(event_name)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_event(self, event_name: str):
        event_names = self.config.get('event_names', [])
        if event_name in event_names:
            return
        event_names.append(event_name)
        await self.config.put('event_names', event_names)

    @remove.command(name='event')
    @checks.admin_or_permissions()
    async def remove_event(self, *, event_name: str):
        self.remove_specific_event(event_name)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_event(self, event_name):
        event_names = self.config.get('event_names', [])
        if event_name in event_names:
            try:
                event_names.remove(event_name)
            except ValueError:
                pass
        await self.config.put('event_names', event_names)

    # TODO create the commands tournament and event for the get_brackets.group
    @get.group(name='brackets', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_brackets(self, *, tournament_names: str):
        if tournament_names is None:
            tournament_names = self.config.get('tournament_names', [])
        else:
            tournament_names = tournament_names.split(" ")
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific_bracket(bracket_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='bracket')
    @checks.admin_or_permissions()
    async def add_bracket(self, *, bracket_ids: str):
        bracket_ids = bracket_ids.split(" ")
        for bracket_id in bracket_ids:
            await self.add_bracket(bracket_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_bracket(self, bracket_id: str):
        bracket_ids = self.config.get('bracket_ids', [])
        if bracket_id in bracket_ids:
            return
        bracket_ids.append(bracket_id)
        await self.config.put('bracket_ids', bracket_ids)

    @remove.command(name='bracket')
    @checks.admin_or_permissions()
    async def remove_bracket(self, *, bracket_id: str):
        self.remove_specific_bracket(bracket_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_bracket(self, bracket_id):
        bracket_ids = self.config.get('bracket_ids', [])
        if bracket_id in bracket_ids:
            try:
                bracket_ids.remove(bracket_id)
            except ValueError:
                pass
        await self.config.put('bracket_ids', bracket_ids)

    # TODO create the commands tournament, event and bracket for the get_sets.group
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
                    await self.add_specific_set(specific_set['id'])
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('tournament')
    @checks.admin_or_permissions()
    async def get_sets_tournament(self, *, tournament_names: str):
        tournament_names = tournament_names.split(" ")
        for tournament_name in tournament_names:
            events = smash.tournament_show_events(tournament_name)
            for event_name in events['events']:
                sets = smash.tournament_show_sets(tournament_name, event_name)
                for specific_set in sets:
                    await self.add_specific_set(specific_set['id'])
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('event')
    @checks.admin_or_permissions()
    async def get_sets_event(self, *, event_names: str):
        event_names = event_names.split(" ")
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            for event_name in event_names:
                sets = smash.tournament_show_sets(tournament_name, event_name)
                for specific_set in sets:
                    await self.add_specific_set(specific_set['id'])
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command('bracket')
    @checks.admin_or_permissions()
    async def get_sets_bracket(self, *, bracket_ids: str):
        bracket_ids = bracket_ids.split(" ")
        for bracket_id in bracket_ids:
            sets = smash.bracket_show_sets(bracket_id)
            for specific_set in sets:
                await self.add_specific_set(specific_set['id'])
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='set')
    @checks.admin_or_permissions()
    async def add_set(self, *, set_ids: str):
        set_ids = set_ids.split(" ")
        for set_id in set_ids:
            await self.add_specific_set(set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def add_displayed_set(self, *, displayed_set_ids: str):
        displayed_set_ids = displayed_set_ids.split(" ")
        for displayed_set_id in displayed_set_ids:
            await self.add_specific_set(displayed_set_id)
            await self.add_specific_displayed_set(displayed_set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def add_specific_set(self, set_id: str):
        set_ids = self.config.get('set_ids', [])
        if set_id in set_ids:
            return
        set_ids.append(set_id)
        await self.config.put('set_ids', set_ids)

    async def add_specific_displayed_set(self, displayed_set_id: str):
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        if displayed_set_id in displayed_set_ids:
            return
        displayed_set_ids.append(displayed_set_id)
        await self.config.put('displayed_set_ids', displayed_set_ids)

    @remove.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def remove_displayed_set(self, *, displayed_set_id: str):
        await self.remove_specific_displayed_set(displayed_set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='set')
    @checks.admin_or_permissions()
    async def remove_set(self, *, set_id: str):
        await self.remove_specific_set(set_id)
        await self.remove_specific_displayed_set(set_id)
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific_set(self, set_id: str):
        set_ids = self.config.get('set_ids', [])
        if set_id in set_ids:
            try:
                set_ids.remove(set_id)
            except ValueError:
                pass
        await self.config.put('set_ids', set_ids)

    async def remove_specific_displayed_set(self, displayed_set_id: str):
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        if displayed_set_id in displayed_set_ids:
            try:
                displayed_set_ids.remove(displayed_set_id)
            except ValueError:
                pass
        await self.config.put('displayed_set_ids', displayed_set_ids)

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

    @remove_all.command(name='sets')
    @checks.is_owner()
    async def remove_all_sets(self):
        set_ids = self.config.get('set_ids', [])
        for i in range(len(set_ids)):
            del set_ids[0]
            await self.config.put('set_ids', set_ids)

    @remove_all.command(name='events')
    @checks.is_owner()
    async def remove_all_events(self):
        event_names = self.config.get('event_names', [])
        for i in range(len(event_names)):
            del event_names[0]
            await self.config.put('event_names', event_names)

    @remove_all.command(name='tournaments')
    @checks.is_owner()
    async def remove_all_tournaments(self):
        tournament_names = self.config.get('tournament_names', [])
        for i in range(len(tournament_names)):
            del tournament_names[0]
            await self.config.put('tournament_names', tournament_names)

            # TODO add setup command
            # TODO add matchups command


def setup(bot):
    bot.add_cog(Smashy(bot))
