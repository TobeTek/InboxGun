from uuid import uuid4


def generate_random_id(length=5):
    random_id = uuid4().hex[:length]
    return random_id
