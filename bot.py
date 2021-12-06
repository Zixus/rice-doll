import discord
from gohanclient import GohanClient

bot = GohanClient()


@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))


@bot.command(aliases=['r'])
async def roll(ctx, *args):
    message = "<@{}> ".format(ctx.author.id) + bot.roll(args)
    await ctx.send(message)


@bot.command(aliases=['gr'])
async def groll(ctx, *args):
    message = "<@{}> ".format(ctx.author.id) + bot.ghost_roll(args)
    await ctx.send(message)


@bot.command()
async def start(ctx, message_id: int):
    to_date = ctx.message.created_at
    from_date = (await ctx.fetch_message(message_id)).created_at

    history = await ctx.channel.history(
        before=to_date,
        after=from_date,
        oldest_first=True
    ).flatten()

    message_list = [{"content": x.content, "author": x.author.id} for x in history]
    [print(x) for x in history]
    # print(message_list)
    await ctx.send("From {} to {}".format(from_date.strftime("%d/%m/%Y, %H:%M"), to_date.strftime("%d/%m/%Y, %H:%M")))