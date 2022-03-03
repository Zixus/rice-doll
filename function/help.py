import discord
from discord.commands import OptionChoice

help_choices = [
    OptionChoice(name="roll", value="roll"),
    OptionChoice(name="sroll", value="sroll"),
    OptionChoice(name="srolld", value="srolld"),
    OptionChoice(name="groll", value="groll"),
    OptionChoice(name="logtxt", value="logtxt"),
    OptionChoice(name="loghtml", value="loghtml"),
    OptionChoice(name="logall", value="logall"),
]


def get_help_embed(command_name):
    if command_name == 'roll':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="roll",
            description="Used for rolling dice",
        )
        embed.add_field(
            name="Alias",
            value="r",
            inline=False,
        ).add_field(
            name="Format",
            value="/r <dice_syntax>",
            inline=False,
        ).add_field(
            name="Example",
            value="/roll 1d20, /r 5d6+3, /r 5d6>=5\n",
            inline=False,
        ).set_footer(
            text="They see me rollin\' They hatin\'"
        )
    elif command_name == 'groll':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="groll",
            description=(
                "Used for rolling dices specialized for ghostbuster TTRPG.\n"
                "Only accepts [Xd6] syntax and can detect ghost dice."
            ),
        )
        embed.add_field(
            name="Alias",
            value="gr",
            inline=False,
        ).add_field(
            name="Format",
            value="/gr <x>d6. x is num of dice to be rolled",
            inline=False,
        ).add_field(
            name="Example",
            value="/groll 1d6, /gr 9d6\n",
            inline=False,
        ).set_footer(
            text="Who you gonna call?"
        )
    elif command_name == 'sroll':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="sroll",
            description=(
                "Used for rolling dices specialized for Shadow of The Demon Lord TTRPG.\n"
                "Accept attribute/modifier accompanied with boon/bane"
            ),
        )
        embed.add_field(
            name="Alias",
            value="sr",
            inline=False,
        ).add_field(
            name="Format",
            value=(
                "/sr <X><B>.\n"
                "X is attribute/modifier, B is bane/boon represented by '+' or '-'.\n"
                "Just see the example."),
            inline=False,
        ).add_field(
            name="Example",
            value="/sroll 13+, /sr 8+++--, /sr -5--+-, /sr +4+6-3\n",
            inline=False,
        ).set_footer(
            text="Have no idea what to put in the footer, sorry."
        )
    elif command_name == 'srolld':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="srolld",
            description=(
                "Just like `sroll` but applying the **determined feat** of the system.\n"
                "Accept attribute/modifier accompanied with boon/bane"
            ),
        )
        embed.add_field(
            name="Alias",
            value="srd",
            inline=False,
        ).add_field(
            name="Format",
            value=(
                "/sr <X><B>.\n"
                "X is attribute/modifier, B is bane/boon represented by '+' or '-'.\n"
                "Just see the example."),
        ).add_field(
            name="Example",
            value="/srolld 13+, /srd 8+++--, /srd -5--+-, /srd +4+6-3\n",
            inline=False,
        ).set_footer(
            text="I am just a normal sroll but more determined."
        )
    elif command_name == 'logtxt':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="logtxt",
            description=(
                "Used to import discord messages on channel or thread into a txt file\n"
            ),
        )
        embed.add_field(
            name="Alias",
            value="lt",
            inline=False,
        ).add_field(
            name="Format",
            value=(
                "/logtxt <begin_message> <end_message>.\n"
                "**begin_message**: message id/link of the beginning of the messages\n"
                "**end_message**: message id/link of the end of the messages\n"
                "\nBoth are optional. If not given, will take the first/last message of channel."
            ),
            inline=False,
        ).add_field(
            name="Example",
            value=(
                "/logtxt 948890569554411530 948891165418217483\n"
                "/lt `https://discord.com/channels/760750245081380/948051638235505`"
            ),
            inline=False,
        ).set_footer(
            text="Have no idea what to put in the footer, sorry."
        )
    elif command_name == 'loghtml':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="logtxt",
            description=(
                "Used to import discord messages on channel or thread into a html file\n"
            ),
        )
        embed.add_field(
            name="Alias",
            value="logweb, lh, lw",
            inline=False,
        ).add_field(
            name="Format",
            value=(
                "/loghtml <begin_message> <end_message>.\n"
                "**begin_message**: message id/link of the beginning of the messages\n"
                "**end_message**: message id/link of the end of the messages\n"
                "\nBoth are optional. If not given, will take the first/last message of channel."
            ),
            inline=False,
        ).add_field(
            name="Example",
            value=(
                "/loghtml 948890569554411530 948891165418217483\n"
                "/lh `https://discord.com/channels/760750245081380/948051638235505`"
            ),
            inline=False,
        ).set_footer(
            text="Have no idea what to put in the footer, sorry."
        )
    elif command_name == 'logall':
        embed = discord.Embed(
            colour=0xD75BF4,
            title="logall",
            description=(
                "Used to import discord message on channel/thread into a txt **and** html file\n"
            ),
        )
        embed.add_field(
            name="Alias",
            value="la",
            inline=False,
        ).add_field(
            name="Format",
            value=(
                "/logall <begin_message> <end_message>.\n"
                "**begin_message**: message id/link of the beginning of the messages\n"
                "**end_message**: message id/link of the end of the messages\n"
                "\nBoth are optional. If not given, will take the first/last message of channel."
            ),
            inline=False,
        ).add_field(
            name="Example",
            value=(
                "/logall 948890569554411530 948891165418217483\n"
                "/la `https://discord.com/channels/760750245081380/948051638235505`"
            ),
            inline=False,
        ).set_footer(
            text="Have no idea what to put in the footer, sorry."
        )
    else:
        embed = discord.Embed(
            colour=0xFF0000,
            title="Command not found"
        )

    return embed
