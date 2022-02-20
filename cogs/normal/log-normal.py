
import re

import discord
from discord.ext import commands

from function.chat_exporter import Logger
from function.util import get_avatar, get_local_timestamp, millis

# Cogs for Log-Related command
class Log(commands.Cog, name="log-normal"):
    def __init__(self, bot):
        self.bot = bot

    # Commands list
    @commands.command(
        name="logtxt",
        description="import a channel to a log in txt format, can accept begin/end message id",
        aliases=["lt"]
    )
    async def logtxt(self, ctx, begin_message_id: int = None, end_message_id: int = None):
        if begin_message_id is None:
            await ctx.send(
                "Please input the message id of the log's beginning!\n"
                "example: /logtxt 923913920327332"
            )
            return

        if end_message_id is None:
            to_date = ctx.message.created_at
        else:
            to_date = (await ctx.fetch_message(end_message_id)).created_at + millis()

        from_date = (await ctx.fetch_message(begin_message_id)).created_at - millis()

        logger = Logger(ctx, from_date, to_date)
        filepath = await logger.log_to_textfile()
        filename = filepath.split("/")[-1].replace(" ", "_")
        filename = re.sub(r"[^A-Za-z\d_\-.]+", "", filename)
        await ctx.send(file=discord.File(filepath, filename=filename))

    # -----


# cog setup
def setup(bot):
    bot.add_cog(Log(bot))
