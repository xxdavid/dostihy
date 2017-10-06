from abc import ABC, abstractmethod

from logger import log_event


class Field(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def visit(self, player, board):
        pass

    def __str__(self):
        return self.name


class Property(Field):
    def __init__(self, name, price):
        self._name = name
        self.owner = None
        self.price = price

    @property
    def name(self):
        return self._name

    def visit(self, player, board):
        if self.owner is None and player.money > self.price:
            wanna_buy = player.strategy.decide_whether_to_buy(player, self)
            if wanna_buy:
                player.money -= self.price
                self.owner = player
                log_event(player, f"bought {self}")
            return True


class Horse(Property):
    def __init__(self, name, price, stable, admissions, new_race_price):
        super().__init__(name, price)
        self.stable = stable
        self.admissions = admissions
        self.races = 0
        self.new_race_price = new_race_price

    def visit(self, player, board):
        if super().visit(player, board):
            return True
        if self.owner is not None:
            if self.owner != player:
                admission = self.admissions[self.races]
                player.money -= admission
                self.owner.money += admission
                log_event(player, f"paid {self.owner} admission of {admission} Kč for visiting {self}")
                return True
            elif self.races < 5:  # owned by the player
                owns_the_whole_stable = all(
                    [field.owner == self.owner
                     for field in board if isinstance(field, Horse) and field.stable == self.stable]
                )
                if owns_the_whole_stable and player.money > self.price:
                    wanna_buy_new_race = \
                        player.strategy.decide_whether_to_buy_race(player, self)
                    if wanna_buy_new_race:
                        player.money -= self.new_race_price
                        self.races += 1
                        log_event(player, f"bought a new race for stable {self.stable}")
                    return True
        return False


class Trainer(Property):
    PRICE = 4000
    ADMISSIONS = [
        1000,
        2000,
        3000,
        4000
    ]

    def __init__(self, trainer_number):
        super().__init__(f"Trainer {trainer_number}", 4000)

    def visit(self, player, board):
        if super().visit(player, board):
            return True
        if self.owner is not None and self.owner != player:
            number_of_trainers_owned = sum(
                (isinstance(field, Trainer) and field.owner == self.owner) for field in board
            )
            admission = self.ADMISSIONS[number_of_trainers_owned - 1]
            player.money -= admission
            self.owner.money += admission
            log_event(player, f"paid {self.owner} admission of {admission} Kč for a training")
            return True
        return False


class StartField(Field):
    @property
    def name(self):
        return "Start"

    def visit(self, player, board):
        pass


class ParkingLot(Field):
    @property
    def name(self):
        return "Parking Lot"

    def visit(self, player, board):
        pass


initialBoard = [
    StartField(),
    Horse("Fantome", 1200, 0, [40, 200, 600, 1800, 3200, 5000], 1000),
    # Finances
    Horse("Gavora", 1200, 0, [40, 200, 600, 1800, 3200, 5000], 1000),
    # Veterinary checkup
    Trainer(1),
    Horse("Lady Anne", 2000, 1, [120, 600, 1800, 5400, 8000, 11000], 1000),
    # Chance
    Horse("Pasek", 2000, 1, [120, 600, 1800, 5400, 8000, 11000], 1000),
    Horse("Koran", 2400, 1, [160, 800, 2000, 6000, 9000, 12000], 1000),
    # "Distanc"
    Horse("Neklan", 2800, 2, [200, 1000, 3000, 9000, 12500, 15000], 2000),
    # Transit
    Horse("Portlancl", 2800, 2, [200, 1000, 3000, 9000, 12500, 15000], 2000),
    Horse("Japan", 2800, 2, [240, 1200, 3600, 10000, 14000, 18000], 2000),
    Trainer(2),
    Horse("Kostrava", 3600, 3, [280, 1400, 4000, 11000, 15000, 19000], 2000),
    # Finances
    Horse("Lukava", 3600, 3, [280, 1400, 4000, 11000, 15000, 19000], 2000),
    Horse("Melák", 4000, 3, [320, 1600, 4400, 12000, 16000, 20000], 2000),
    ParkingLot(),
    Horse("Grifel", 4400, 4, [360, 1800, 5000, 14000, 17000, 21000], 3000),
    # Chance
    Horse("Mohyla", 4400, 4, [360, 1800, 5000, 14000, 17000, 21000], 3000),
    Horse("Metál", 4800, 4, [400, 2000, 6000, 15000, 18000, 22000], 3000),
    Trainer(3),
    Horse("Tara", 5200, 5, [440, 2200, 6600, 16000, 19500, 23000], 3000),
    Horse("Furioso", 5200, 5, [440, 2200, 6600, 16000, 19500, 23000], 3000),
    # Stable
    Horse("Genius", 5600, 5, [580, 2400, 7200, 17000, 20500, 24000], 3000),
    # Suspicion of doping
    Horse("Shagga", 6000, 6, [500, 2600, 7800, 18000, 22000, 25500], 4000),
    Horse("Dahoman", 6000, 6, [500, 2600, 7800, 18000, 22000, 25500], 4000),
    # Finances
    Horse("Gira", 6400, 6, [560, 3000, 9000, 20000, 24000, 28000], 4000),
    Trainer(4),
    # Chance
    Horse("Narcius", 7000, 7, [700, 3500, 10000, 22000, 26000, 30000], 4000),
    # Veterinary checkup
    Horse("Napoli", 8000, 7, [1000, 4000, 12000, 28000, 34000, 40000], 4000),
]
