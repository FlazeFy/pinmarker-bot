
def get_sender_id(event):
    source_type = event.source.type

    if source_type == "group":
        senderId = event.source.group_id
    elif source_type == "user":
        senderId = event.source.user_id
    elif source_type == "room":
        senderId = event.source.room_id

    return senderId