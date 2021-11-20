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
        help_desc = "Usage: `{0}roll <syntax> [#<comments>]` or `{0}r <syntax> [#<comments>]`\nNo, this bot **can't do math**.\nRefer to https://pypi.org/project/d20/ for the rolling syntax. =w=)7"
        return help_desc.format(self.command_prefix)

    def roll(self, args):  
        try:
            parse = re.sub(" +", "", args[0]) #remove spaces
            result = str(d20.roll(parse))
            comment = ""
            if(len(args) > 1):
                comment = " ".join(args[1:])
            return comment + " : " + result
        except Exception as e:
            response = "\n" + str(type(e)) + ':\n' + str(e) + "\n\n"
            return response
            