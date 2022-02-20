import asyncio
import io
import os
import re
import sys

import discord
from discord.ext import commands

from function.chat_exporter import Logger
from function.util import get_avatar, get_local_timestamp, millis
from db.sequel import Database

sys.path.insert(1, "./DiscordChatExporterPy")
import chat_exporter  # noqa: E402

DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL"))
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_DB = os.getenv("MYSQL_DB")

# Cogs for Log-Related command
class Log(commands.Cog, name="log-normal"):
    def __init__(self, bot):
        self.bot = bot

    # Commands list
    @commands.command(
        name="logtxt",
        description="import a channel messages to a log in txt format, can accept begin/end message id",
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

    @commands.command(
        name="loghtml",
        description="import a channel messages to a log in html format, can accept begin/end message id",
        aliases=["lh", "logweb", "lw"]
    )
    async def loghtml(self, ctx, begin_message_id=None, end_message_id=None, filename=None):
        end_time = None
        begin_time = None

        if begin_message_id:
            begin_time = (await ctx.fetch_message(begin_message_id)).created_at - millis()

        if end_message_id:
            end_time = (await ctx.fetch_message(end_message_id)).created_at + millis()

        transcript = await chat_exporter.export(
            ctx.channel,
            ctx.guild,
            limit=None,
            begin_time=begin_time,
            end_time=end_time,
            set_timezone="Asia/Jakarta",
        )

        if transcript is None:
            return

        if not filename:
            filename = (
                f"{ctx.guild.name}-{ctx.message.channel.name}_"
                f"{get_local_timestamp(begin_time)} - {get_local_timestamp(end_time)}"
            )
            filename = filename.replace(" ", "_")
            filename = re.sub(r"[^A-Za-z\d_\-.]+", "", filename)

        transcript = await self.replace_avatar(
            await get_avatar(transcript=transcript), trancript=transcript
        )
        await asyncio.sleep(1)
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()), filename=f"transcript-{filename}.html"
        )

        await ctx.send(file=transcript_file)

    # -----
    
    # Non-commands method
    async def replace_avatar(self, file, trancript):
        transcript_string = trancript
        dump_channel = self.bot.get_channel(DUMP_CHANNEL)
        db = Database()
        for f in file:
            avatar_file = discord.File(f["image"], filename=f["filename"])
            data = db.get_avatar_after(f["avatar_before"])
            if data:
                attachment = data[0]
            else:
                sent_image = await dump_channel.send(file=avatar_file)
                attachment = sent_image.attachments[0].url
                db.insert_avatar(f["avatar_before"], attachment)
                await asyncio.sleep(1)
            transcript_string = transcript_string.replace(f["avatar_string"], attachment)
        db.close
        return transcript_string
    # -----
# cog setup
def setup(bot):
    bot.add_cog(Log(bot))
