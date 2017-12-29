from termcolor import colored

enabled = True


def log(text, color=None):
    if enabled:
        print(colored(text, color))


def log_event(player, event):
    log(f"{player} {event}.", player.color)
