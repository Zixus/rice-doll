import discord
from gohanclient import GohanClient
from logger import Log

bot = GohanClient()

@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))

@bot.command(aliases=['r'])
async def roll(ctx, *args):
    if(len(args)<1):
        await ctx.send("Please input a roll argument")
        return
    message = "<@{}> ".format(ctx.author.id) + bot.roll(args)
    await ctx.send(message)
 