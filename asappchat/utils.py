import random

def generate_random_str(length, allowed_chars):
    return ''.join(random.SystemRandom().choice(allowed_chars) for _ in range(length))
