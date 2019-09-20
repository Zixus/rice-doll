from bs4 import BeautifulSoup
import requests
from requests import Session
import urllib.parse
import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

CATEGORIES = {
	'action' : '0',
	'ancestry': '1',
	'background': '2',
	'class': '3',
	'condition': '4',
	'equipment': '5',
	'feat': '6',
	'hazard': '7',
	'monster': '8',
	'ritual': '9',
	'rule': '10',
	'setting': '11',
	'skill': '12',
	'spell': '13',
	'find' : '0=on&ctl00%24MainContent%24TableList%241=on&ctl00%24MainContent%24TableList%242=on&ctl00%24MainContent%24TableList%243=on&ctl00%24MainContent%24TableList%244=on&ctl00%24MainContent%24TableList%245=on&ctl00%24MainContent%24TableList%246=on&ctl00%24MainContent%24TableList%247=on&ctl00%24MainContent%24TableList%248=on&ctl00%24MainContent%24TableList%249=on&ctl00%24MainContent%24TableList%2410=on&ctl00%24MainContent%24TableList%2411=on&ctl00%24MainContent%24TableList%2412=on&ctl00%24MainContent%24TableList%2413'
}

ACTIONS = {
	'Free Action' : '<:freeaction:622904630015295498>',
	'Single Action' : '<:oneaction:622904693328445442>',
	'Two Actions' : '<:twoaction:622904763343962114>',
	'Three Actions' : '<:threeaction:622904811263885353>',
	'Reaction' : '<:reaction:622904859519090710>'
}

COMMANDS = [
	'action',
	'ancestry',
	'background',
	'class',
	'condition',
	'equipment',
	'feat',
	'hazard',
	'monster',
	'ritual',
	'rule',
	'setting',
	'skill',
	'spell',
	'find',
	'help'
]

# NUMBERING = {
# 	"1" : "A",
# 	"2" : "B",
# 	"3" : "C",
# 	"4" : "D",
# 	"5" : "E"
# }

# SELECTION_EMOJI = ['🇦', '🇧', '🇨', '🇩', '🇪']

def extract_tag_by_id (text, tag_id):
	soup = BeautifulSoup(text, features="html.parser")
	res = soup.find(id=tag_id)
	return res

def get_search_output (category, txt_search):
	s = Session()
	r = s.get("https://2e.aonprd.com/Search.aspx")
	view_state_value = extract_tag_by_id(r.text, "__VIEWSTATE")['value']
	view_state = urllib.parse.quote(view_state_value, safe='')
	view_state_gen_value = extract_tag_by_id(r.text, "__VIEWSTATEGENERATOR")['value']
	view_state_gen = urllib.parse.quote(view_state_value, safe='')
	request_data = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=' + view_state + '&__VIEWSTATEGENERATOR=' + view_state_gen + '&ctl00%24MainContent%24txtSearch=' + txt_search + '&ctl00%24MainContent%24btnSearch=Search+Now&ctl00%24MainContent%24TableList%24' + CATEGORIES[category] + '=on'
	header = {
		'Host': '2e.aonprd.com',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://2e.aonprd.com/Search.aspx'
	}
	s.headers = header
	r = s.post("https://2e.aonprd.com/Search.aspx", data=request_data)
	search_output = extract_tag_by_id(r.text, "ctl00_MainContent_SearchOutput")
	search_output = search_output.find_all('a')
	results = []
	for result in search_output:
		results.append({
			'title' : result.string,
			'link' : result.get('href')
			})
	return (results)

def extract_desc (raw_soup):
	description = {}
	raw_desc = raw_soup.contents
	header = raw_desc.pop(0)
	action = header.find(attrs={'alt' : True})
	level = header.span
	description['title'] = ""
	if action is not None:
		description['title'] += " " + ACTIONS[action.get('alt')]
	if level is not None:
		description['title'] += " (" + level.get_text() + ")"
	desc = ""
	traits = []

	while ((len(raw_desc) > 0) and (raw_desc[0].name != "h1") and (raw_desc[0].name != "h2") and (raw_desc[0].name != "h3")):
		buff = raw_desc.pop(0)
		if (buff.name == "a" or buff.name == "u"):
			desc += "__" + buff.get_text() + "__"
		elif (buff.name == "b"):
			desc += "**" + buff.get_text() + "**"
		elif (buff.name == "i"):
			desc += "*" + buff.get_text() + "*"
		elif (buff.name == "br"):
			desc += "\n"
		elif (buff.name == "hr"):
			desc += "\n\n"
		elif (buff.name == "ul"):
			i = 0
			while (i < len(buff.contents)):
				desc += "- " + buff.contents[i].get_text() + "\n"
				i += 1
		elif (buff.name == "span"):
			traits.append(buff.get_text())
		elif (buff.name == "img" and buff.get("alt") is not None):
			raw_desc.pop(0)
			desc += ACTIONS[buff.get("alt")]
		elif (buff.name is None):
			desc += buff
	description['desc'] = desc
	for trait in traits:
		description['desc'] = trait + " " + description['desc']
	if (len(traits) > 0):
		description['desc'] = "**Traits** " + description['desc']
	return (description)

def get_detailed_output (link):
	with requests.Session() as s:
		s = Session()
		r = s.get("https://2e.aonprd.com/" + link)
		detailed_output = extract_tag_by_id(r.text, "ctl00_MainContent_DetailedOutput")
		desc = extract_desc(detailed_output)
		desc['url'] = "https://2e.aonprd.com/" + link
		return (desc)

def make_embed_pages(search_res, category, items_per_page):
	max_page = int(len(search_res) / items_per_page)
	if (len(search_res) % items_per_page != 0):
		max_page += 1
	embed_pages = []
	find_category = category
	if (find_category == "find"):
		find_category = "all categories"
	buff = ""
	i = 0
	while (i < len(search_res)):
		buff += str(i+1) + ". " + search_res[i]['title'] + "\n"
		i += 1
		if (((i % items_per_page) == 0) or (i == len(search_res))):
			page_num = int(i / items_per_page)
			if (i == len(search_res)):
				page_num = max_page
			embed_pages.append(discord.Embed(title = "Search Result in `" + find_category + "` (" + "Page " + str(page_num) + "/" + str(max_page) + ")", description = buff ).set_footer(text = "Type `<` or `>` to navigate between pages; Type the number to select"))
			buff = ""
	return (embed_pages)

class NethysClient(discord.Client):
	prefix = "?"

	async def on_ready(self):
		print('Logged on as {0}'.format(self.user))
		# await client.change_presence(status=discord.Status.idle, activity=discord.Game("Maintenances"))
		await client.change_presence(activity=discord.Game("?help"))


	async def on_message(self, message):
		if (message.content.startswith(self.prefix)):
			channel = message.channel
			command_line = message.content.split(" ")
			command = command_line[0][1:]
			if (command in COMMANDS):
				if (command == "help"):
					help_text = "**?action** [search key]\n**?ancestry** [search key]\n**?background** [search key]\n**?class** [search key]\n**?condition** [search key]\n**?equipment** [search key]\n**?feat** [search key]\n**?hazard** [search key]\n**?monster** [search key]\n**?ritual** [search key]\n**?rule** [search key]\n**?setting** [search key]\n**?skill** [search key]\n**?spell** [search key]\n**?find** [search key]\n**?help**"
					await message.channel.send(embed=discord.Embed(title="Command List",description=help_text))
				elif (len(command_line) > 1):
					arg = command_line[1:]
					search = arg.pop(0)
					while (len(arg) > 0):
						search += " " + arg.pop(0)
					search_res = get_search_output(command, search)
					if (len(search_res) > 0):
						embeds = make_embed_pages(search_res, command, 10)
						response = await message.channel.send(embed=embeds[0])

						def check(msg):
							return message.author == msg.author

						i = 0

						while (True):
							try:
								msg = await self.wait_for("message", timeout=15, check=check)
							except asyncio.TimeoutError:
								await response.edit(embed=discord.Embed(description="Search timed out"))
								break
							else:
								if ((msg.content == "<") and (i > 0)):
									await response.delete()
									try:
										await msg.delete()
									except discord.Forbidden:
										pass
									i -= 1
									response = await channel.send(embed=embeds[i])
								elif ((msg.content == ">") and (i < len(embeds)-1)):
									await response.delete()
									try:
										await msg.delete()
									except discord.Forbidden:
										pass
									i += 1
									response = await channel.send(embed=embeds[i])
								else:
									try:
										search_index = int(msg.content)-1
										embed_data = get_detailed_output(search_res[search_index]['link'])
										embed = discord.Embed(title = search_res[search_index]['title'] + embed_data['title'], description= embed_data['desc'][0:2000], url = embed_data['url'])
										await response.delete()
										try:
											await msg.delete()
										except discord.Forbidden:
											pass
										await channel.send(embed=embed)
										break
									except (ValueError, IndexError) as e:
										continue
					else:
						await channel.send("Cannot find " + search + " in " + command)
			elif (len(message.content) > 1):
				await message.channel.send(embed=discord.Embed(description= "Not a command. Type ?help to list available commands."))
client = NethysClient()
client.run(TOKEN)
