r"""
Chat Exporter Class
"""
from pathlib import Path
import os
from .util import get_local_timestamp


class Logger:

    TIME_FORMAT = "%d-%m-%Y, %H:%M"
    LIMIT = 100

    def __init__(self, ctx, from_date, to_date):
        self.ctx = ctx
        self.from_date = from_date
        self.to_date = to_date

    def log_info(self):
        log_info = {
            "guild_icon": self.ctx.guild.icon_url if self.ctx.guild.icon else "",
            "server_name": self.ctx.guild.name,
            "category_name": self.ctx.message.channel.category.name
            if self.ctx.message.channel.category else None,
            "channel_name": self.ctx.message.channel.name,
            "from_date": self.from_date.strftime(self.TIME_FORMAT),
            "to_date": self.to_date.strftime(self.TIME_FORMAT)
        }
        return log_info

    async def message_list(self):
        toggle = True
        message_list = []
        history = []
        while toggle or len(history) >= self.LIMIT:
            history = await self.ctx.channel.history(
                limit=self.LIMIT,
                before=self.to_date,
                after=self.from_date,
                oldest_first=True
            ).flatten()
            message_list.extend(history)
            self.from_date = history[-1].created_at
            toggle = False
        return message_list

    def header(self):
        log_info = self.log_info()
        header = Path('function/header.html').read_text().format(
            log_info["server_name"],
            log_info["channel_name"]
        )
        return header

    def body_info(self):
        log_info = self.log_info()
        body_info = Path('function/body_info.html').read_text().format(
            log_info["guild_icon"],
            log_info["server_name"],
            log_info["category_name"],
            log_info["channel_name"],
            log_info["from_date"],
            log_info["to_date"]
        )
        return body_info

    async def message(self):
        message_list = await self.message_list()
        messages = [(message.author.display_name, message.content) for message in message_list]
        print(messages)

    async def log_to_textfile(self):
        log_begin_timestamp = get_local_timestamp(self.from_date)
        log_end_timestamp = get_local_timestamp(self.to_date)
        guild_name = self.ctx.guild.name
        channel_name = self.ctx.message.channel.name

        filename = f"{guild_name}-{channel_name} {log_begin_timestamp} - {log_end_timestamp}.txt"
        folderpath = f"./{guild_name}/"
        filepath = os.path.join(folderpath, filename)

        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        message_list = await self.message_list()

        with open(filepath, 'w+') as f:
            for message in message_list:
                f.write(f"[{get_local_timestamp(message.created_at)}]"
                        f" {message.author.display_name}: {message.content}\n")

        return filepath
