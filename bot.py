from gohanclient import GohanClient
import discord

bot = GohanClient()

@bot.command()
async def help(ctx):
    await ctx.send(embed=discord.Embed(description=bot.help()))

@bot.command()
async def roll(ctx, *args):
    await ctx.send(bot.roll(args))