feedback_active = set()

def add_to_feedback(user_id):
    feedback_active.add(user_id)

def remove_from_feedback(user_id):
    feedback_active.discard(user_id)
