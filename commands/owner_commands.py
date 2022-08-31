from constants import HRC_CHARACTERS, PERSONAL_GUILD_ID, STADIUM_GUILD_ID, VERSIONS, ALIASES, BTT_STAGES
from formulas import get_char_name

from db import connect

from interactions import Client, CommandContext, Permissions, Option, OptionType

# TODO: verify insertions are valid. eg. make sure it's ntsc1.02 and not ntsc 1.02
# can cross-ref with constants

# HELPER functions

# GENERAL
#def check_sources(sources: list ) -> :
#    check_src_sql = 

# HRC



def register_owner_commands(bot: Client):
    @bot.command(
        name='add-btt-record',
        description='Add BTT record',
        scope=[PERSONAL_GUILD_ID], #, STADIUM_GUILD_ID],
        options=[
            Option(
                name='character',
                description='Choose your character',
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name='stage',
                description='Choose your stage',
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name='player',
                description='Player',
                type=OptionType.STRING,
                required=True,
            ),
            # require at least one of the two
            Option(
                name='score',
                description='Score decimal',
                type=OptionType.NUMBER,
                required=True,                
            ),
            Option(
                name='sources',
                description='sources',
                type=OptionType.STRING,
                required=False,                
            ),
            Option(
                name='date',
                description='yyyy-mm-dd',
                type=OptionType.STRING,
                required=False,                
            ),
            Option(
                name='tas',
                description='tas',
                type=OptionType.BOOLEAN,
                required=False,                
            ),
            Option(
                name='emulator',
                description='Played on emu',
                type=OptionType.BOOLEAN,
                required=False,                
            ),
            Option(
                name='debug',
                description='Played on debug',
                type=OptionType.BOOLEAN,
                required=False,                
            ),
            Option(
                name='tags',
                description='add tags (case sensitive, CSV)',
                type=OptionType.STRING,
                required=False,                
            ),
            Option(
                name='ver',
                description='version',
                type=OptionType.STRING,
                required=False,                
            ),
        ],

        #default_member_permissions=Permissions.ADMINISTRATOR    
    )

    async def _add_btt_record(ctx: CommandContext, **kwargs):
        if ctx.author.id != str(199563168345882624):
            return None
        char_input = kwargs.get("character")
        char = get_char_name(char_input, ALIASES)
        # TODO: raise error if character isn't in database
        # TODO: allow for zelda and sheik individual records 
        if char not in HRC_CHARACTERS:
            description = f'Please select a valid char ({char} invalid)'
            await ctx.send(description, ephemeral=True)
        stage_input = kwargs.get('stage')
        stage = get_char_name(stage_input, ALIASES)
        if stage not in BTT_STAGES:
            description = f'Please select a valid stage ({stage} invalid)'
            await ctx.send(description, ephemeral=True)
        player = kwargs.get("player")
        # TODO: have to raise some sort of exception if player doesn't exist.... in database table?
        
        score = kwargs.get("score")

        sources = kwargs.get('sources', '') 
        # TODO: add check_source function and update source function
        
        date = kwargs.get('date', '') # default system time so it auto corrects to UTC+00:00, when you're submitting. otherwise unknown
        # TODO: add check_date function

        is_tas = kwargs.get('tas', False)
        is_emulator = kwargs.get('emulator', True)
        is_debug = kwargs.get('debug', False)
        tags = kwargs.get('tags', '') 
        # TODO: make a check tags function and update tags function

        ver = kwargs.get('ver', '')
        # TODO: add regex for all of these (e.g. match NTSC1.02 with ntsc1.02 with NTSC 1.02 etc.)
        if ver not in VERSIONS:
            raise ValueError(f'Please select a valid version')
        
        score_str = '{:.2f}'.format(score)

        sources_str = "{" + sources + "}"
        tags_str = "{" + tags + "}"

        conn = connect()
        sql_q = f"INSERT INTO btt_table VALUES('{char}', '{stage}', '{player}', {score_str}, '{sources_str}', '{date}', {is_tas}, {is_emulator}, {is_debug}, '{tags_str}', '{ver}');"
        cur = conn.cursor()
        cur.execute(sql_q)


        video = sources.split(',')[0]
        conn.commit()
        description = f'Added BTT record: {char}/{stage} - {score_str} by {player} at <{video}>'
        await ctx.send(description)





    # add hrc record
    # add 10mm record
    # add event record