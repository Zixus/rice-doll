from gohanclient import GohanClient
import discord

bot = GohanClient()

@bot.command()
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))

@bot.command()
async def roll(ctx, *args):
    message = "<@{}> : ".format(ctx.author.id)+str(bot.roll(args))
    await ctx.send(message)