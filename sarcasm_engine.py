import random

def get_sarcastic_message():
    messages = [
        "Oh wow, you're a real keyboard ninja, aren't you?",
        "Slow down! The turtle’s about to sue you for emotional damage.",
        "Your keyboard called. It needs a vacation.",
        "This isn’t a Formula 1 race. It’s TortoiseLang.",
        "Congratulations! You’ve earned the ‘Too Fast, Too Curious’ award.",
        "Nice try, Shakespeare. But the turtle disagrees.",
        "Coding at warp speed? Bold. Wrong, but bold.",
        "You're typing faster than the turtle can think. Rude.",
        "Ever heard of slow food? This is slow code.",
        "Your code has officially outpaced human patience."
    ]
    return random.choice(messages)

def get_poetic_output():
    haikus = [
        # Original Creative Haikus
        "Code like a whisper,\nSoftly flowing, line by line—\nErrors fear silence.",
        "Slow and steady types,\nWisdom in every keystroke,\nThe bug stays asleep.",
        "Haste is the foe here,\nTurtles preach divine rhythm,\nPause. Now type again.",
        "A line of logic,\nNot rushed but born with meaning,\nLike rain on still ponds.",
        "In slow typing's glow,\nA turtle watches, amused,\nScripting elegance.",

        # Public Domain / Inspired Additions
        "Over the keyboard,\nFingers rush, but thoughts delay—\nTurtle shakes his head.",
        "Write one line slowly,\nRead it like a morning breeze—\nThe code flows with peace.",
        "Why do you hurry?\nThe turtle’s still on line two—\nAnd he wrote a gem.",
        "Infinite wisdom—\nLies not in speed, but in pause.\nReflect, type, repeat.",
        "The wind does not rush,\nYet moves mountains patiently.\nSo should your fingers.",

        # Meta-funny ones
        "Beneath blinking lights,\nFast fingers breed fast errors—\nTurtle sighs again.",
        "A furious tap,\nBrings forth compiler fury—\nPatience is your shield.",
        "Racing through functions,\nSyntax collapses in fear—\nSlow is beautiful.",
        "Shift. Return. Escape.\nNone will help your case here.\nSlow down or regret.",
        "The screen glares at you,\nSilently judging your haste—\nSlow. Compose. Retry."
    ]
    return random.choice(haikus)
