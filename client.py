import os
import asyncio
from dotenv import load_dotenv

import discord
import d20

class GohanClient(discord.Client):
	prefix = "/"

	async def on_ready(self):
		await self.change_presence(activity=discord.Game("/help"))
		print('Logged on as {0}'.format(self.user))
		
	async def on_message(self, message):
		content = "<@{}> : ".format(message.author.id)
		try:
			if (message.content.startswith(self.prefix)):
				args = message.content[1:].split(" ", 1)
				if (args[0] == "r") or (args[0] == "roll"):
					result = d20.roll(args[1])
					content += str(result)
					await message.channel.send(content)
				elif (args[0] == "h") or (args[0] == "help"):
					await message.channel.send(embed=discord.Embed(description="Usage: `/roll <syntax>` or `/r <syntax>`\n Refer to https://pypi.org/project/d20/ for the rolling syntax"))

		except Exception as e:
			content += "\n" + str(type(e)) + ':\n' + str(e)
			await message.channel.send(content)

if __name__ == "__main__":
	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	bot = GohanClient()
	bot.run(TOKEN)