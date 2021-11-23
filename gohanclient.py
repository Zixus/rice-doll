import discord
from discord.ext import commands
import d20
import re


class GohanClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            help_command=None,
            case_insensitive=True,
            description="Rice Doll",
            allowed_mentions=discord.AllowedMentions(
                roles=False, users=True, everyone=False
            ),
            intents=discord.Intents.all()
        )

    def run(self, token):
        super().run(token)

    def help(self):
        help_desc = """
            Usage: `{0}roll <syntax> [#<comments>]` or `{0}r <syntax> [#<comments>]`\n
            No, this bot **can't do math**.\n
            Refer to https://pypi.org/project/d20/ for the rolling syntax. =w=)7"
            """
        return help_desc.format(self.command_prefix)

    def roll(self, args):
        try:
            parse = re.sub(" +", "", args[0])  # remove spaces
            result = str(d20.roll(parse))
            comment = ""
            if(len(args) > 1):
                comment = " ".join(args[1:])
            return comment + " : " + result
        except Exception as e:
            response = "\n" + str(type(e)) + ':\n' + str(e) + "\n\n"
            return response

    def ghost_roll(self, args):
        try:
            ghost_warning = ""
            comment = ""

            parse = re.sub(" +", "", args[0])  # remove spaces
            result = d20.roll(parse)

            root = result.expr
            d6_dice = d20.utils.dfs(
                root, lambda node: isinstance(node, d20.Dice) and node.size == 6)

            if d6_dice is None:
                raise Exception("No d6 roll in the expression!")

            last_die = d6_dice.values[d6_dice.num-1]
            if last_die.number == 6:
                last_die.force_value(0)
                ghost_warning = "| Uh-oh, **GHOST DIE!** 👻"
            if(len(args) > 1):
                comment = " ".join(args[1:])
            return comment + " : " + str(result) + ghost_warning
        except Exception as e:
            response = "\n" + str(type(e)) + ':\n' + str(e) + "\n\n"
            return response
