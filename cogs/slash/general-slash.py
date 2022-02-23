import random
import os

import discord
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

guild_ids = list(map(int, os.getenv("SLASH_GUILD_IDS").split(",")))


class General(commands.Cog, name="general-slash"):
    def __init__(self, bot):
        self.bot = bot

    # Command list
    @commands.slash_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
        guild_ids=guild_ids
    )
    async def serverinfo(self, ctx: ApplicationContext) -> None:
        """
        Get some useful (or not) information about the server.
        :param interaction: The application command interaction.
        """
        roles = [role.name for role in ctx.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{ctx.guild}",
            color=0x9C84EF
        )
        if ctx.guild.icon:
            embed.set_thumbnail(
                url=ctx.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=ctx.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=ctx.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(ctx.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(ctx.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {ctx.guild.created_at}"
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
        guild_ids=guild_ids,
    )
    async def invite(self, ctx: ApplicationContext) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        :param interaction: The application command interaction.
        """
        embed = discord.Embed(
            description=("Invite me by clicking [here]"
                         "(https://discordapp.com/oauth2/authorize?&client_id="
                         "524500535651467264&scope=bot+applications.commands&permissions=8)."),
            color=0xD75BF4
        )
        try:
            await ctx.author.send(embed=embed)
            await ctx.respond("I sent you a private message!")
        except discord.Forbidden:
            await ctx.respond(embed=embed)

    @commands.slash_command(
        name="8ball",
        description="Ask any question to the bot.",
        guild_ids=guild_ids,
    )
    async def eight_ball(
        self,
        ctx: ApplicationContext,
        question: Option(
            str,
            "A question you want to ask",  # noqa: F722
            required=True,
        )
    ) -> None:
        """
        Ask any question to the bot.
        :param interaction: The application command interaction.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.",
                   "Without a doubt.", "Yes - definitely.", "As I see, yes.",
                   "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                   "Reply hazy, try again.", "Ask again later.",
                   "Better not tell you now.", "Cannot predict now.",
                   "Concentrate and ask again later.", "Don't count on it.",
                   "My reply is no.", "My sources say no.", "Outlook not so good.",
                   "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await ctx.respond(embed=embed)

    # -----


def setup(bot):
    bot.add_cog(General(bot))
