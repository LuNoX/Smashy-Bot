import pysmash
from .utils import config, checks
from discord.ext import commands
import discord
import time

smash = pysmash.SmashGG()


class Smashy:
    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('smashy.json', loop=bot.loop)

    @commands.group(pass_context=True, no_pm=True)
    async def add(self, ctx):
        """Adds an item(s) to the database."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @add.command(name='tournament')
    @checks.admin_or_permissions()
    async def add_tournament(self, *tournament_names: str):
        """Adds a tournament(s) to the database."""
        for tournament_name in tournament_names:
            await self.add_specific(tournament_name, 'tournament_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='event')
    @checks.admin_or_permissions()
    async def add_event(self, *event_names: str):
        """Adds an event(s) to the database."""
        for event_name in event_names:
            await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='bracket')
    @checks.admin_or_permissions()
    async def add_bracket(self, *bracket_ids: str):
        """Adds a bracket(s) to the database."""
        for bracket_id in bracket_ids:
            await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='set')
    @checks.admin_or_permissions()
    async def add_set(self, *set_ids: str):
        """Adds a set(s) to the database."""
        for set_id in set_ids:
            await self.add_specific(set_id, 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @add.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def add_displayed_set(self, *displayed_set_ids: str):
        """Adds a displayed set(s) to the database."""
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

    @commands.group(pass_context=True, no_pm=True, aliases=['delete', 'drop'])
    async def remove(self, ctx):
        """Removes an item from the database."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @remove.command(name='tournament')
    @checks.admin_or_permissions()
    async def remove_tournament(self, *tournament_names: str):
        """Removes a tournament(s) from the database."""
        for tournament_name in tournament_names:
            await self.remove_specific(tournament_name, 'tournament_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='event')
    @checks.admin_or_permissions()
    async def remove_event(self, *event_names: str):
        """Removes an event(s) from the database."""
        for event_name in event_names:
            await self.remove_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='bracket')
    @checks.admin_or_permissions()
    async def remove_bracket(self, *bracket_ids: str):
        """Removes a brackets(s) from the database."""
        for bracket_id in bracket_ids:
            await self.remove_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove.command(name='set', pass_context=True)
    @checks.admin_or_permissions()
    async def remove_set(self, ctx, *set_ids: str):
        """Removes a sets(s) from the database."""
        for set_id in set_ids:
            await self.remove_specific(set_id, 'set_ids')
        await ctx.invoke(self.remove_displayed_set, *set_ids)

    @remove.command(name='displayed_set')
    @checks.admin_or_permissions()
    async def remove_displayed_set(self, *displayed_set_ids: str):
        """Removes a displayed set(s) from the database."""
        for displayed_set_id in displayed_set_ids:
            await self.remove_specific(displayed_set_id, 'displayed_set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_specific(self, specific: str, specific_db_key: str):
        specifics = self.config.get(specific_db_key, [])
        if specific in specifics:
            try:
                specifics.remove(specific)
            except ValueError:
                pass
        await self.config.put(specific_db_key, specifics)

    @remove.group(name='all', invoke_without_command=True)
    @checks.is_owner()
    async def remove_all(self):
        """Removes everything from the database."""
        await self.remove_all_specific('displayed_set_ids')
        await self.remove_all_specific('set_ids')
        await self.remove_all_specific('event_names')
        await self.remove_all_specific('tournament_names')
        await self.remove_all_specific('bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='tournaments')
    @checks.is_owner()
    async def remove_all_tournaments(self):
        await self.remove_all_specific('tournament_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='events')
    @checks.is_owner()
    async def remove_all_events(self):
        """Removes all events from the database."""
        await self.remove_all_specific('event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='brackets')
    @checks.is_owner()
    async def remove_all_brackets(self):
        """Removes all brackets from the database."""
        await self.remove_all_specific('bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='sets')
    @checks.is_owner()
    async def remove_all_sets(self):
        """Removes all sets from the database."""
        await self.remove_all_specific('set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @remove_all.command(name='displayed_sets')
    @checks.is_owner()
    async def remove_all_displayed_sets(self):
        """Removes all displayed sets from the database."""
        await self.remove_all_specific('displayed_set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    async def remove_all_specific(self, specific_db_key: str):
        # I know this is ugly but list.remove(list_id) didn't work properly for some reason
        # This also can probably be done way easier by using the config.remove or config.put functions,
        # but I only realised that afterwards...
        # TODO make remove_all pretty
        specifics = self.config.get(specific_db_key, [])
        for i in range(len(specifics)):
            del specifics[0]
        await self.config.put(specific_db_key, specifics)

    # TODO catch exceptions
    # TODO make this work with multiple tournaments
    @commands.group(pass_context=True, no_pm=True)
    async def get(self, ctx):
        """Querys the API for items and adds them to the database."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @get.group(name='events', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_events(self):
        """Querys the API for events and adds them to the database.

        The query is based on the tournament(s) that are saved in the database."""
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            try:
                event_names = smash.tournament_show_events(tournament_name)
            except Exception as e:
                await self.bot.say('\N{PISTOL}')
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            for event_name in event_names['events']:
                await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_events.group(name='tournament')
    @checks.admin_or_permissions()
    async def get_events_tournament(self, *tournament_names: str):
        """Querys the API for events and adds them to the database.

        The query is based on the given tournament name(s)."""
        for tournament_name in tournament_names:
            try:
                event_names = smash.tournament_show_events(tournament_name)
            except Exception as e:
                await self.bot.say('\N{PISTOL}')
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            for event_name in event_names['events']:
                await self.add_specific(event_name, 'event_names')
        await self.bot.say('\N{OK HAND SIGN}')

    @get.group(name='brackets', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_brackets(self):
        """Querys the API for brackets and adds them to the database.

        The query is based on the tournament(s) and event(s) that are saved in the database."""
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                try:
                    brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                except Exception as e:
                    await self.bot.say('\N{PISTOL}')
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_brackets.command(name='tournament')
    @checks.admin_or_permissions()
    async def get_brackets_tournament(self, *tournament_names: str):
        """Querys the API for brackets and adds them to the database.

        The query is based on the given tournament name(s)."""
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_brackets.command(name='event')
    @checks.admin_or_permissions()
    async def get_brackets_event(self, *event_names: str):
        """Querys the API for brackets and adds them to the database.

        The query is based on the tournament(s) saved in the database and the given event name(s)."""
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            for event_name in event_names:
                try:
                    brackets = smash.tournament_show_event_brackets(tournament_name, event_name)
                except Exception as e:
                    await self.bot.say('\N{PISTOL}')
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
                for bracket_id in brackets['bracket_ids']:
                    await self.add_specific(bracket_id, 'bracket_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get.group(name='sets', invoke_without_command=True)
    @checks.admin_or_permissions()
    async def get_sets(self):
        """Querys the API for sets and adds them to the database.

        The query is based on the tournament(s) and event(s) saved in the database."""
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            event_names = self.config.get('event_names', [])
            for event_name in event_names:
                try:
                    sets = smash.tournament_show_sets(tournament_name, event_name)
                except Exception as e:
                    await self.bot.say('\N{PISTOL}')
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
                for specific_set in sets:
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command(name='tournament')
    @checks.admin_or_permissions()
    async def get_sets_tournament(self, *tournament_names: str):
        """Querys the API for sets and adds them to the database.

        The query is based on the given tournament name(s)."""
        for tournament_name in tournament_names:
            try:
                events = smash.tournament_show_events(tournament_name)
            except Exception as e:
                await self.bot.say('\N{PISTOL}')
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            for event_name in events['events']:
                try:
                    sets = smash.tournament_show_sets(tournament_name, event_name)
                except Exception as e:
                    await self.bot.say('\N{PISTOL}')
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
                for specific_set in sets:
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command(name='event')
    @checks.admin_or_permissions()
    async def get_sets_event(self, *event_names: str):
        """Querys the API for sets and adds them to the database.

        The query is based on the tournament(s) saved in the database and the given event name(s)."""
        tournament_names = self.config.get('tournament_names', [])
        for tournament_name in tournament_names:
            for event_name in event_names:
                try:
                    sets = smash.tournament_show_sets(tournament_name, event_name)
                except Exception as e:
                    await self.bot.say('\N{PISTOL}')
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
                for specific_set in sets:
                    await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @get_sets.command(name='bracket')
    @checks.admin_or_permissions()
    async def get_sets_bracket(self, *bracket_ids: str):
        """Querys the API for sets and adds them to the database.

        The query is based on the given bracket id(s)."""
        for bracket_id in bracket_ids:
            try:
                sets = smash.bracket_show_sets(bracket_id)
            except Exception as e:
                await self.bot.say('\N{PISTOL}')
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            print(sets)
            for specific_set in sets:
                await self.add_specific(specific_set['id'], 'set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @commands.group(pass_context=True, no_pm=True, hidden=True)
    async def smashy(self, ctx):
        """This is a test command for development purposes."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid subcommand passed: {0.subcommand_passed}'.format(ctx))

    @smashy.command(name='test', pass_context=True)
    @checks.admin_or_permissions()
    async def smashy_test(self, ctx):
        """This is a test command for development purposes."""
        await ctx.invoke(self.remove_all_displayed_sets)
        await ctx.invoke(self.matchups)
        await self.bot.say('test successful')

    @commands.command(name='setup', pass_context=True)
    @checks.admin_or_permissions()
    async def setup(self, ctx, *tournament_names: str):
        """Sets up the database based on the given tournament name(s)"""
        # TODO make setup more efficient by calling the get.commands with the db data instead of calling the api
        await self.bot.say('Setting up tournament...')
        await ctx.invoke(self.add_tournament, *tournament_names)
        await self.bot.say('Configuring events...')
        await ctx.invoke(self.get_events)
        await self.bot.say('Configuring brackets...')
        await ctx.invoke(self.get_brackets)
        await self.bot.say('Configuring sets...')
        await ctx.invoke(self.get_sets)
        await self.bot.say('Setup complete!')

    # TODO make it respond in a dedicated channel
    # TODO make doubles work
    # TODO add a clock that invokes this command
    @checks.mod_or_permissions()
    @commands.group(name='matchups', invoke_without_command=True, pass_context=True)
    async def matchups(self, ctx):
        """Prints all upcoming matchups."""
        await ctx.invoke(self.matchups_timesensitive, False)

    @matchups.command(name='timesensitive', pass_context=True)
    async def matchups_timesensitive(self, ctx, timecheck: bool=True):
        """Prints all upcoming matchups except ones where the starting time has not been reached yet."""
        displayed_set_ids = self.config.get('displayed_set_ids', [])
        displayed_set_ids_as_set = set(displayed_set_ids)
        set_ids = self.config.get('set_ids', [])
        set_ids_as_set = set(set_ids)
        not_displayed_set_ids = set_ids_as_set - displayed_set_ids_as_set
        print(not_displayed_set_ids)
        for not_displayed_set_id in list(not_displayed_set_ids):
            not_displayed_set = smash.show('set', not_displayed_set_id, 'sets')
            if not_displayed_set['loserId'] is not None or not_displayed_set['winnerId'] is not None:
                await self.add_specific(not_displayed_set_id, 'displayed_set_ids')
            elif not_displayed_set['entrant1Id'] is not None and not_displayed_set['entrant2Id'] is not None:
                if timecheck:
                    has_started_yet = False
                    start = not_displayed_set['startAt']
                    if start is not None and start < time.time():
                        has_started_yet = True
                else:
                    has_started_yet = True
                if has_started_yet:
                    event_name = smash.show('event', not_displayed_set['eventId'], 'event')['typeDisplayStr']
                    if event_name.endswith(' '):  # Smash.gg doesnt say doubles in the name, instead there is a space
                        event_name += 'Doubles'
                    entrant_1_name = self.determine_player_name(not_displayed_set['entrant1Id'], ctx.message.server)
                    entrant_2_name = self.determine_player_name(not_displayed_set['entrant2Id'], ctx.message.server)
                    message = '{} and {} your {} match is up!'.format(entrant_1_name, entrant_2_name, event_name)
                    await self.bot.say(message)
                    await self.add_specific(not_displayed_set_id, 'displayed_set_ids')
        await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(pass_context=True)
    async def next(self, ctx):
        """Updates the database with the most recent sets and then prints the upcoming matchups timesensitively."""
        await self.bot.say('Getting sets')
        await ctx.invoke(self.get_sets)
        await self.bot.say('Printing matchups')
        await ctx.invoke(self.matchups_timesensitive)

    # TODO: add a lookuptable for all smash.gg and discord names
    @staticmethod
    def determine_player_name(entrant_id: str, server: discord.Server):
        entrant_name = smash.show('entrant', entrant_id, 'entrants')
        entrant_name = entrant_name['name']
        if ' / ' not in entrant_name:  # Smash.gg separates the player names of a Doubles team with ' / '
                                        #  this could lead to errors with 2 users named "man / 1" and "man"
            entrant_member = server.get_member_named(entrant_name)
            if entrant_member is None:
                return entrant_name
            else:
                return entrant_member.mention
        else:
            entrant_names = entrant_name.split(' / ')
            entrant_members = ''
            first = True
            for entrant_name in entrant_names:
                entrant_member = server.get_member_named(entrant_name)
                if entrant_member is None:
                    entrant_member = entrant_name
                else:
                    entrant_member = entrant_member.mention
                # TODO: Make this work with more than 2 people
                if first:
                    first = False
                else:
                    entrant_members += ' / '
                entrant_members += entrant_member
            return entrant_members


def setup(bot):
    bot.add_cog(Smashy(bot))
