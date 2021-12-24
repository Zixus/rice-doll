import discord
from function.chat_exporter import Logger
from gohanclient import GohanClient

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
