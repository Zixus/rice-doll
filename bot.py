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
