import discord
from discord.ext import commands
from custom_Stringifier import BoolStringifier

import d20
import re
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s')

arithmeticOps = ['+', '-', '*', '/']
booleanOps = ['=', '<', '<=', '>', '>=']


class GohanClient(commands.Bot):
    errorMsg = "Something is wrong. Please check your input"

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

    def getDice(self, roll, die=0):
        if die == 0:
            return d20.utils.dfs(
                roll.expr, lambda node: isinstance(node, d20.Dice))
        return d20.utils.dfs(
                roll.expr, lambda node: isinstance(node, d20.Dice) and node.size == die)

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
            comment = ""
            result = self._roll(parse)

            if(len(args) > 1):
                comment = " ".join(args[1:])
            return comment + " : " + str(result)
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    def bool_roll(self, args):
        try:
            comment = ""
            parse = args[0]
            curOps = ""

            for ops in booleanOps:
                if(ops in parse):
                    curOps = ops
                parse = re.sub(" "+ops, "", parse)  # remove spaces

            if curOps in booleanOps:
                target = int(parse.split(curOps, 1)[1])
                result, success = self._bool_roll(parse, curOps, target)

                if(len(args) > 1):
                    comment = " ".join(args[1:])
                return comment + " : " + str(result) + " = " + str(success) + " success"
            else:
                return self.roll(args)
        except Exception as e:
            logging.warning(
                "[BoolRoll] " + str(type(e)) + " : " + str(e) + ". Passing to vanilla roll")
            return self.roll(args)

    def _roll(self, parse):
        try:
            result = d20.roll(parse)
            return result
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    def _bool_roll(self, parse, curOps, target):
        try:
            success = 0
            result = d20.roll(parse, stringifier=BoolStringifier())
            dice = self.getDice(result)

            if curOps in booleanOps:
                if dice is None:
                    raise Exception("No d6 dice found in the expression!")

                for die in dice.values:
                    if curOps == '=':
                        if die.number == target:
                            success = success + 1
                    if curOps == '<':
                        if die.number < target:
                            success = success + 1
                    if curOps == '<=':
                        if die.number <= target:
                            success = success + 1
                    if curOps == '>':
                        if die.number > target:
                            success = success + 1
                    if curOps == '>=':
                        if die.number >= target:
                            success = success + 1

                return result, success
            else:
                return self._roll(parse)
        except Exception as e:
            logging.warning(
                "[BoolRoll] " + str(type(e)) + " : " + str(e) + ". Passing to vanilla roll")
            return self._roll(parse)

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
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    def shadow_roll(self, args):
        try:
            roll_string = '1d20'
            comment = ""

            rollinput = args[0]

            # Add modifier
            numVal = int(re.search(r'\d+', rollinput).group())

            if rollinput[0] == '+':
                mod = numVal
                rollinput = rollinput.lstrip('+-')
            elif rollinput[0] == '-':
                mod = -numVal
                rollinput = rollinput.lstrip('+-')
            else:
                mod = numVal-10

            if mod != 0:
                if mod < 0:
                    roll_string += '-'
                else:
                    roll_string += '+'
                roll_string += str(abs(mod))

            # Add Bane and Boon
            boonNumSyntax = re.search(r'\+\d+', rollinput)
            baneNumSyntax = re.search(r'\-\d+', rollinput)

            if boonNumSyntax:
                boonVal = boonNumSyntax.group()
                rollinput.replace(boonVal, '')
                rollinput += boonVal[0] * int(boonVal[1])

            if baneNumSyntax:
                baneVal = baneNumSyntax.group()
                rollinput.replace(baneVal, '')
                rollinput += baneVal[0] * int(baneVal[1])

            boon_bane_mod = rollinput.count("+") - rollinput.count("-")
            if boon_bane_mod != 0:
                if boon_bane_mod < 0:
                    roll_string += '-'
                else:
                    roll_string += '+'
                roll_string += str(abs(boon_bane_mod)) + 'd6kh1'

            result = d20.roll(roll_string)

            if(len(args) > 1):
                comment = " ".join(args[1:])
            return comment + " : " + str(result)
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg
