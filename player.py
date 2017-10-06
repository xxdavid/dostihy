class Player:
    def __init__(self, name, strategy, color=None):
        self.name = name
        self.strategy = strategy
        self.money = 30000
        self.position = 0
        self.color = color

    def pay(self, amount, receiver):
        self.money -= amount
        receiver.money += amount

    def __str__(self):
        return self.name
