import discord
import shlex
from discord.ext import commands

from db.sequel import AliasDB


# Cogs for Alias-Related command
class Alias(commands.Cog, name="alias-normal"):
    def __init__(self, bot):
        self.bot = bot

    # Commands list
    @commands.command(
        name="alias",
        description="add user alias"
    )
    async def create_user_alias(self, ctx, name, *, command):
        user_id = ctx.message.author.id
        if not ctx.bot.get_command(command.split()[0]):
            await ctx.send("Command not exist.")
            return
        db = AliasDB()
        db.upsert_user_alias(name=name, user_id=user_id, command=command)
        db.close()
        await ctx.send(f'User alias `{name}` created for command `{command}`')

    @commands.command(
        name="servalias",
        description="add server alias",
        aliases=['serveralias']
    )
    async def create_server_alias(self, ctx, name, *, command):
        server_id = ctx.guild.id
        if not ctx.bot.get_command(command.split()[0]):
            await ctx.send("Command not exist.")
            return
        db = AliasDB()
        db.upsert_server_alias(name=name, server_id=server_id, command=command)
        db.close()
        await ctx.send(f'Server alias `{name}` created for command `{command}`')

    @commands.command(
        name="alias_list",
        description="get all alias",
        aliases=['alist']
    )
    async def select_alias(self, ctx):
        # TODO: pagination. might be unused.
        user_id = ctx.message.author.id
        server_id = ctx.guild.id
        db = AliasDB()
        user_aliases = db.select_user_alias(user_id=user_id)
        user_aliases_list = ', '.join([x[0] for x in user_aliases])
        server_aliases = db.select_server_alias(server_id=server_id)
        server_aliases_list = ', '.join([x[0] for x in server_aliases])
        embed = discord.Embed(
            title="List of Aliases"
        )
        embed.add_field(
            name="User Aliases",
            value=user_aliases_list
        )
        embed.add_field(
            name="Server Alias",
            value=server_aliases_list
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="call",
        description="call alias",
        aliases=[';']
    )
    async def call_alias(self, ctx, name, *call_args):
        user_id = ctx.message.author.id
        server_id = ctx.guild.id
        db = AliasDB()
        macro = db.get_user_command(name=name, user_id=user_id)
        if macro is None:
            macro = db.get_server_command(name=name, server_id=server_id)
        if macro is None:
            return
        macro_split = shlex.split(macro[0])
        command = macro_split[0]
        args = macro_split[1:] if len(macro_split) > 1 else []
        args.extend(call_args)
        command_obj = self.bot.get_command(command)
        if command_obj is not None:
            await ctx.message.delete()
            await ctx.invoke(command_obj, *args)
    # TODO: Delete, Rename, Check Command

    # -----

    # Non-commands method

    # -----


# cog setup
def setup(bot):
    bot.add_cog(Alias(bot))
