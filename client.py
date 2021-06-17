import os
import re
import asyncio
from dotenv import load_dotenv

import discord
import d20

class GohanClient(discord.Client):
	prefix = "/"
	help_desc = "Usage: `{0}roll <syntax> [#<comments>]` or `{0}r <syntax> [#<comments>]`\nNo, this bot **can't do math**.\nRefer to https://pypi.org/project/d20/ for the rolling syntax"

	async def on_ready(self):
		await self.change_presence(activity=discord.Game("{0}help or {0}h".format(self.prefix)))
		print('Logged on as {0}'.format(self.user))
		
	async def on_message(self, message):
		response = "<@{}> : ".format(message.author.id)
		try:
			if (message.content.startswith(self.prefix)) and (not message.author.bot):
				content = message.content[len(self.prefix):]
				args = content.split(" ", 1)
				if (args[0] == "r") or (args[0] == "roll"):
					args = args[1].split("#", 1) #args[0] as roller string, args[1] as comment
					args[0] = re.sub(" +", "", args[0])
					if len(args) > 1:
						response += args[1] + " = "
					result = d20.roll(args[0])
					response += str(result)
					await message.channel.send(response)
				elif (args[0] == "h") or (args[0] == "help"):
					await message.channel.send(embed=discord.Embed(description=self.help_desc.format(self.prefix)))

		except Exception as e:
			response += "\n" + str(type(e)) + ':\n' + str(e) + "\n\n"
			await message.channel.send(embed=discord.Embed(description=response + self.help_desc.format(self.prefix)))

if __name__ == "__main__":
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	bot = GohanClient()
	bot.run(TOKEN)