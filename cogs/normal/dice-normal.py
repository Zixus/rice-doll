import d20
import logging
import re

from discord import InvalidArgument
from custom_stringifier import BoolStringifier
from discord.ext import commands

ARITHMETIC_OPS = ['+', '-', '*', '/']
BOOLEAN_OPS = ['=', '==', '<', '<=', '>', '>=']


# Cogs for Dice-Related command
class Dice(commands.Cog, name="dice-normal"):
    def __init__(self, bot):
        self.bot = bot
        self.errorMsg = "Something is wrong. Please check your input"

    # Commands list
    @commands.command(
        name="roll",
        description="command for rolling",
        aliases=['r'],
    )
    async def roll(self, ctx, *args):
        if (len(args) < 1):
            await ctx.send("Please input a roll argument")
            return

        print(self.resolve_bool_roll(args))
        message = "<@{}> ".format(ctx.author.id) + self.resolve_bool_roll(args)
        await ctx.send(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content[0] == '`':
            return

        if self.find_inline_roll(message.content):
            reply = "<@{}> ".format(message.author.id) + '\n'
            for x in self.find_inline_roll(message.content):
                reply += self.resolve_bool_roll(x.split()).replace(': ', '', 1) + '\n'
            await message.channel.send(reply)

    @commands.command(
        name="groll",
        description="command for rolling dice for ghost buster",
        aliases=['gr'],
    )
    async def groll(self, ctx, *args):
        if len(args) < 1:
            await ctx.send("Please input a roll argument")
            return
        message = "<@{}> ".format(ctx.author.id) + self.ghost_roll(args)
        await ctx.send(message)

    @commands.command(
        name="sroll",
        description="command for rolling dice for shadow of demon lord",
        aliases=['sr'],
    )
    async def sroll(self, ctx, *args):
        if len(args) < 1:
            await ctx.send("Please input a roll argument")
            return
        message = "<@{}> ".format(ctx.author.id) + self.shadow_roll(args, False)
        await ctx.send(message)

    @commands.command(
        name="srolld",
        description="command for rolling dice for shadow of demon lord with detemined status",
        aliases=['srd'],
    )
    async def srolld(self, ctx, *args):
        if len(args) < 1:
            await ctx.send("Please input a roll argument")
            return
        message = "<@{}> ".format(ctx.author.id) + self.shadow_roll(args, True)
        await ctx.send(message)

    # -----

    # Non-commands method
    def get_dice(self, roll, die=0):
        if die == 0:
            return d20.utils.dfs(
                roll.expr, lambda node: isinstance(node, d20.Dice))
        return d20.utils.dfs(
                roll.expr, lambda node: isinstance(node, d20.Dice) and node.size == die)

    def resolve_roll(self, args):
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

    def resolve_bool_roll(self, args):
        try:
            comment = ""
            parse = args[0]
            curOps = ""

            for ops in BOOLEAN_OPS:
                if(ops in parse):
                    curOps = ops
                parse = re.sub(" "+ops, "", parse)  # remove spaces

            if curOps in BOOLEAN_OPS:
                target = int(parse.split(curOps, 1)[1])
                result, success = self._bool_roll(parse, curOps, target)

                if(len(args) > 1):
                    comment = " ".join(args[1:])
                return comment + " : " + str(result) + " = " + str(success) + " success"
            else:
                return self.resolve_roll(args)
        except Exception as e:
            logging.warning(
                "[BoolRoll] " + str(type(e)) + " : " + str(e) + ". Passing to vanilla roll")
            return self.resolve_roll(args)

    def _bool_roll(self, parse, curOps, target):
        try:
            success = 0

            # Handling = operator
            if curOps == '=':
                leftExp, rightExp = parse.split('=')
                parse = leftExp + "==" + rightExp

            result = d20.roll(parse, stringifier=BoolStringifier())
            dice = self.get_dice(result)

            if curOps in BOOLEAN_OPS:
                if dice is None:
                    raise Exception("No d6 dice found in the expression!")

                for die in dice.values:
                    if curOps == '=' or curOps == '==':
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

    def _roll(self, parse):
        try:
            result = d20.roll(parse)
            return result
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    def ghost_roll(self, args):
        ghost_warning = ""
        comment = ""

        parse = re.sub(" +", "", args[0])  # remove spaces
        result = d20.roll(parse)

        root = result.expr
        d6_dice = d20.utils.dfs(
            root, lambda node: isinstance(node, d20.Dice) and node.size == 6)

        if d6_dice is None:
            raise InvalidArgument("No d6 roll in the expression!")

        last_die = d6_dice.values[d6_dice.num-1]
        if last_die.number == 6:
            last_die.force_value(0)
            ghost_warning = "| Uh-oh, **GHOST DIE!** 👻"
        if(len(args) > 1):
            comment = " ".join(args[1:])
        return comment + " : " + str(result) + ghost_warning

    def shadow_roll(self, args, determined):
        try:
            roll_string = "1d20"
            comment = ""

            rollinput = args[0]

            # Add modifier
            numVal = int(re.search(r"\d+", rollinput).group())

            if rollinput[0] == "+":
                mod = numVal
                rollinput = rollinput.lstrip("+-")
            elif rollinput[0] == "-":
                mod = -numVal
                rollinput = rollinput.lstrip("+-")
            else:
                mod = numVal - 10

            if mod != 0:
                if mod < 0:
                    roll_string += "-"
                else:
                    roll_string += "+"
                roll_string += str(abs(mod))

            # Add Bane and Boon
            boonNumSyntax = re.search(r"\+\d+", rollinput)
            baneNumSyntax = re.search(r"\-\d+", rollinput)

            if boonNumSyntax:
                boonVal = boonNumSyntax.group()
                rollinput = rollinput.replace(boonVal, "")
                rollinput += boonVal[0] * int(boonVal[1:])

            if baneNumSyntax:
                baneVal = baneNumSyntax.group()
                rollinput = rollinput.replace(baneVal, "")
                rollinput += baneVal[0] * int(baneVal[1:])

            boon_bane_mod = rollinput.count("+") - rollinput.count("-")
            if boon_bane_mod != 0:
                if boon_bane_mod < 0:
                    roll_string += "-"
                else:
                    roll_string += "+"
                boon_string = "d6"
                if determined:
                    boon_string += "ro1"
                boon_string += "kh1"
                roll_string += str(abs(boon_bane_mod)) + boon_string

            result = d20.roll(roll_string)

            if len(args) > 1:
                comment = " ".join(args[1:])
            return comment + " : " + str(result)
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    def find_inline_roll(self, str):
        return re.findall(r'\[\[(.+?)\]\]', str)
    # -----


# cog setup
def setup(bot):
    bot.add_cog(Dice(bot))
