from emit import _emit

def show_turtle_rage():
    turtle = r"""
               _____     ______
             < x   x >  /      \ 
              \  -  /  |  O   O |
              /     \  |   ∆    |
             |       | \______/
            /| |   | |\
           /_|_|___|_|_\
            /_/     \_\
    🐢 RAGE MODE: Turtle is not amused by your speed.
    """
    _emit(turtle) 

def show_turtle_just_right():
    turtle = r"""
         _____
       < ^   ^ >
        \  -  /
        /     \
       |  o o  |
       |   ∆   |
       \_______/
    🐢 Turtle is content with your pace.
    """
    _emit(turtle)

def show_turtle_too_slow():
    turtle = r"""
         _____
       < -   - >
        \  _  /
        /     \
       |  . .  |
       |   -   |
       \_______/
    🐢 Turtle is falling asleep. Type a bit faster!
    """
    _emit(turtle)
