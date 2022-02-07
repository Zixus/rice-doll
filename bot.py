import asyncio
import discord
from function.chat_exporter import Logger
from gohanclient import GohanClient
from function.util import get_avatar, get_local_timestamp, millis
import re
import io
import sys

import os
from dotenv import load_dotenv
sys.path.insert(1, './DiscordChatExporterPy')
import chat_exporter  # noqa: E402


TIMESTAMP_TEMPLATE = "%d/%m/%Y, %H:%M"
load_dotenv('.env')
DUMP_CHANNEL = int(os.getenv('DUMP_CHANNEL'))

bot = GohanClient()


# Non-Command Function
async def replace_avatar(file, trancript):
    transcript_string = trancript
    dump_channel = bot.get_channel(DUMP_CHANNEL)
    for f in file:
        avatar_file = discord.File(f['image'], filename=f['filename'])
        sent_image = await dump_channel.send(file=avatar_file)
        attachment = sent_image.attachments[0].url
        await asyncio.sleep(1)
        transcript_string = transcript_string.replace(f['avatar_string'], attachment)
    return transcript_string

# Command Function


@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))


@bot.command(aliases=['r'])
async def roll(ctx, *args):
    if(len(args) < 1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.bool_roll(args)
    await ctx.send(message)


@bot.command(aliases=['gr'])
async def groll(ctx, *args):
    if(len(args) < 1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.ghost_roll(args)
    await ctx.send(message)


@bot.command(aliases=['sr'])
async def sroll(ctx, *args):
    if(len(args) < 1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.shadow_roll(args)
    await ctx.send(message)


@bot.command()
async def boolRoll(ctx, *args):
    if(len(args) < 1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.bool_roll(args)
    await ctx.send(message)


@bot.command()
async def start(ctx, begin_message_id: int = None, end_message_id: int = None):
    if begin_message_id is None:
        await ctx.send("Please input the message id of the log's beginning!\n"
                       "example: /start 923913920327332")
        return

    if end_message_id is None:
        to_date = ctx.message.created_at
    else:
        to_date = (await ctx.fetch_message(end_message_id)).created_at + millis()

    from_date = (await ctx.fetch_message(begin_message_id)).created_at - millis()

    logger = Logger(ctx, from_date, to_date)
    await logger.message()
    await ctx.send(f" From {from_date.strftime(TIMESTAMP_TEMPLATE)}"
                   f" to {to_date.strftime(TIMESTAMP_TEMPLATE)} ")


@bot.command(aliases=['lt'])
async def logtxt(ctx, begin_message_id: int = None, end_message_id: int = None):
    if begin_message_id is None:
        await ctx.send("Please input the message id of the log's beginning!\n"
                       "example: /logtxt 923913920327332")
        return

    if end_message_id is None:
        to_date = ctx.message.created_at
    else:
        to_date = (await ctx.fetch_message(end_message_id)).created_at + millis()

    from_date = (await ctx.fetch_message(begin_message_id)).created_at - millis()

    logger = Logger(ctx, from_date, to_date)
    filepath = await logger.log_to_textfile()
    filename = filepath.split("/")[-1].replace(" ", "_")
    filename = re.sub(r'[^A-Za-z\d_\-.]+', '', filename)
    await ctx.send(file=discord.File(filepath, filename=filename))


@bot.command(aliases=['lh', 'logweb', 'lw'])
async def loghtml(ctx, begin_message_id=None, end_message_id=None, filename=None):
    end_time = None
    begin_time = None

    if begin_message_id:
        begin_time = (await ctx.fetch_message(begin_message_id)).created_at - millis()

    if end_message_id:
        end_time = (await ctx.fetch_message(end_message_id)).created_at + millis()

    transcript = await chat_exporter.export(ctx.channel, ctx.guild, limit=None,
                                            begin_time=begin_time, end_time=end_time,
                                            set_timezone="Asia/Jakarta"
                                            )

    if transcript is None:
        return

    if not filename:
        filename = (f"{ctx.guild.name}-{ctx.message.channel.name}_"
                    f"{get_local_timestamp(begin_time)} - {get_local_timestamp(end_time)}")
        filename = filename.replace(" ", "_")
        filename = re.sub(r'[^A-Za-z\d_\-.]+', '', filename)

    transcript = await replace_avatar(await get_avatar(transcript=transcript), trancript=transcript)
    await asyncio.sleep(1)
    transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                   filename=f"transcript-{filename}.html")

    await ctx.send(file=transcript_file)
