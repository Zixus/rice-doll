import os
import asyncio
from dotenv import load_dotenv

import discord
import d20

class GohanClient(discord.Client):
	prefix = "="

	async def on_ready(self):
		await self.change_presence(activity=discord.Game("=help"))
		print('Logged on as {0}'.format(self.user))
		
	async def on_message(self, message):
		content = "<@{}> : ".format(message.author.id)
		try:
			if (message.content.startswith(self.prefix)):
				args = message.content[len(self.prefix):].split(" ", 1)
				if (args[0] == "r") or (args[0] == "roll"):
					args = args[1].split("#", 1)
					if len(args) > 1:
						content += args[1] + " = "
					result = d20.roll(args[0])
					content += str(result)
					await message.channel.send(content)
				elif (args[0] == "h") or (args[0] == "help"):
					await message.channel.send(embed=discord.Embed(description="Usage: `r!roll <syntax>` or `r!r <syntax>`\n Refer to https://pypi.org/project/d20/ for the rolling syntax"))

		except Exception as e:
			content += "\n" + str(type(e)) + ':\n' + str(e)
			await message.channel.send(content)

if __name__ == "__main__":
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	bot = GohanClient()
	bot.run(TOKEN)