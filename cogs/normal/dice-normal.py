import d20
import logging
import re

from custom_stringifier import BoolStringifier
from discord.ext import commands

ARITHMETIC_OPS = ['+', '-', '*', '/']
BOOLEAN_OPS = ['=', '<', '<=', '>', '>=']


# Cogs for Dice-Related command
class Dice(commands.Cog, name="dice-normal"):
    def __init__(self, bot):
        self.bot = bot

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

        message = "<@{}> ".format(ctx.author.id) + self.resolve_bool_roll(args)
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
        print("_bool_roll")
        try:
            success = 0
            result = d20.roll(parse, stringifier=BoolStringifier())
            dice = self.get_dice(result)

            if curOps in BOOLEAN_OPS:
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

    def _roll(self, parse):
        try:
            result = d20.roll(parse)
            return result
        except Exception as e:
            logging.error(str(type(e)) + " : " + str(e))
            return self.errorMsg

    # -----


# cog setup
def setup(bot):
    bot.add_cog(Dice(bot))
