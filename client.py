""""
Credit Template Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
"""

import os
import platform
from dotenv import load_dotenv


import discord
from discord import Interaction
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

ENV = os.getenv("ENV")

if ENV == 'dev':
    load_dotenv('.env.dev')
else:
    load_dotenv('.env')

intents = discord.Intents.all()

bot = Bot(
        command_prefix="/",
        intents=intents,
        case_insensitive=True,
        description="Rice Doll",
        allowed_mentions=discord.AllowedMentions(
            roles=False, users=True, everyone=False
        ),
    )


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"Pycord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    # automatically load slash and normal command on respective folders
    load_commands("slash")
    load_commands("normal")


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message,
    with or without the prefix :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: Interaction) -> None:
    """
    The code in this event is executed every time a slash command has been
    *successfully* executed :param interaction: The slash command that has been executed.
    """
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} "
        f"(ID: {interaction.guild.id}) by {interaction.user} (ID: {interaction.user.id})"
        )


@bot.event
async def on_slash_command_error(interaction: Interaction, error: Exception) -> None:
    """
    The code in this event is executed every time a valid slash command catches an error
    :param interaction: The slash command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        print("A user without proper permission tried to execute a command.")
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    raise error


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.message.guild.name} "
        f"(ID: {context.message.guild.id}) by {context.message.author} "
        f"(ID: {context.message.author.id})"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

# Run the bot with the token
bot.run(os.getenv('DISCORD_TOKEN'))
