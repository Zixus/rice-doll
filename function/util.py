from datetime import timedelta
import re

LOCAL_OFFSET_HOUR = 7
TIME_FORMAT = "%d-%m-%Y %H.%M"


def get_local_timestamp(ts):
    local_ts = ts + timedelta(hours=LOCAL_OFFSET_HOUR)
    return local_ts.strftime(TIME_FORMAT)


def millis():
    return timedelta(milliseconds=1)


def sub_discord_markdown(str, conf):
    str = re.sub(r'```([^```]*)```', fr'{conf["codeblock"][0]}\1{conf["codeblock"][1]}', str)
    str = re.sub(r'\*\*([^\*\*]*)\*\*', fr'{conf["bold"][0]}\1{conf["bold"][1]}', str)
    str = re.sub(r'__([^__]*)__', fr'{conf["underline"][0]}\1{conf["underline"][1]}', str)
    str = re.sub(r'\*([^\*]*)\*', fr'{conf["italic"][0]}\1{conf["italic"][1]}', str)
    str = re.sub(r'_([^_]*)_', fr'{conf["italic"][0]}\1{conf["italic"][1]}', str)
    str = re.sub(r'~~([^~~]*)~~', fr'{conf["strike"][0]}\1{conf["strike"][1]}', str)
    str = re.sub(r'`([^`]*)`', fr'{conf["onelinecode"][0]}\1{conf["onelinecode"][1]}', str)
    str = re.sub(r'^> (.*)', fr'{conf["quoteblock"]}\1', str)  # for the first quote block
    str = re.sub(r'\n> (.*)', fr'\n{conf["quoteblock"]}\1', str)  # for any quote block afte
    return str


def strip_markdown_txt(str):
    config = dict({
        'bold': ('', ''),
        'codeblock': ('', ''),
        'italic': ('', ''),
        'onelinecode': ('', ''),
        'quoteblock': '',
        'strike': ('', ''),
        'underline': ('', ''),
    })
    str = re.sub(r'<:(.*):\d+>', r':\1:', str)
    str = re.sub(r'~~([^~~]*)~~', lambda match: fr'{striken(match.group(1))}', str)
    return sub_discord_markdown(str, config)


def map_mention(s, mentions):
    mention_dict = dict()

    for m in mentions:
        mention_dict[str(m.id)] = m.display_name

    return re.sub(r'<@!(\d+)>', lambda match: fr'@{mention_dict[match.group(1)]}', s)


def striken(text):
    return ''.join(t+chr(822) for t in text)
