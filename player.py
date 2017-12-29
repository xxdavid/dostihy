from typing import Optional

from strategies import Strategy


class Player:
    def __init__(self, name: str, strategy: Strategy, color: Optional[str] = None):
        self.name = name
        self.strategy = strategy
        self.money = 30000
        self.position = 0
        self.color = color
        self.suspended = False

    def pay(self, amount: int, receiver: 'Player'):
        self.money -= amount
        receiver.money += amount

    def __str__(self):
        return self.name
