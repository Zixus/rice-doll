r"""
Chat Exporter Class
"""
from pathlib import Path


class Logger:
    def __init__(self, ctx, message_id):
        self.ctx = ctx
        self.message_id = message_id
        self.to_date = ctx.message.created_at
        self.from_date = (await ctx.fetch_message(message_id)).created_at

    def log_info(self):
        log_info = {
            "guild_icon": self.ctx.guild.icon_url if self.ctx.guild.icon else "",
            "server_name": self.ctx.guild.name,
            "category_name": self.ctx.message.channel.category.name if self.ctx.message.channel.category else None,
            "channel_name": self.ctx.message.channel.name,
            "from_date": self.from_date.strftime("%d/%m/%Y, %H:%M"),
            "to_date": self.to_date.strftime("%d/%m/%Y, %H:%M")
        }
        return log_info

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

