import re

async def send_long_message(channel, message):
    for i in range(0, len(message), 2000):
        await channel.send(message[i:i+2000])

def convert_html_to_discord_chat(message):
    html_pattern = r'<(\/?)(b|i|u|s|code|pre)>'

    replacements = {
        'b': '**',
        'i': '*',
        'u': '__',
        's': '~~',
        'code': '`',
        'pre': '```'
    }

    def repl(match):
        tag = match.group(2)
        if tag in replacements:
            return replacements[tag]
        return match.group(0)

    return re.sub(html_pattern, repl, message)

def filter_out(tokens, list_out):
    return ' '.join([token for token in tokens if token not in list_out])