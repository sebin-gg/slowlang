import random

messages = [
    "Whoa there, Shakespeare. Try again... slower.",
    "Calm down, coder. This isn't a race.",
    "Your keyboard needs a break.",
    "Did someone say turbo mode?",
    "ERROR: Too much caffeine detected!"
]

def get_random_sarcasm():
    return random.choice(messages)
