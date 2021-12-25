import discord
from function.chat_exporter import Logger
from gohanclient import GohanClient
from function.util import millis
import re

TIMESTAMP_TEMPLATE = "%d/%m/%Y, %H:%M"

bot = GohanClient()


@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))


@bot.command(aliases=['r'])
async def roll(ctx, *args):
    if(len(args) < 1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.roll(args)
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
async def start(ctx, message_id: int):
    to_date = ctx.message.created_at
    from_date = (await ctx.fetch_message(message_id)).created_at
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
