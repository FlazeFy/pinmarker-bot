
def send_long_message(message, max_length=4096):
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]