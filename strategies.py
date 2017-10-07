from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def decide_whether_to_buy_property(self, player, property):
        pass

    @abstractmethod
    def decide_whether_to_buy_race(self, player, horse):
        pass


class BuyAllStrategy(Strategy):
    """Buys everything it has money for."""
    def decide_whether_to_buy_property(self, player, property):
        return True

    def decide_whether_to_buy_race(self, player, horse):
        return True


class BuyNothingStrategy(Strategy):
    """Buys literally nothing. """
    def decide_whether_to_buy_property(self, player, property):
        return False

    def decide_whether_to_buy_race(self, player, horse):
        return False


class CautiousStrategy(Strategy):
    """
    Buys offered stuff only if player's amount of money
    won't be below the threshold after the purchase.
    """
    def __init__(self, threshold):
        self.threshold = threshold

    def decide_whether_to_buy_property(self, player, property):
        return (player.money - property.price) > self.threshold

    def decide_whether_to_buy_race(self, player, horse):
        return (player.money - horse.new_race_price) > self.threshold


class HumanStrategy(Strategy):
    def decide_whether_to_buy_property(self, player, property):
        key = input(f"Do you want to buy {property} for {property.price} Kč? [Y/n] ")
        return key == "y" or key is "Y" or key == ""

    def decide_whether_to_buy_race(self, player, horse):
        key = input(f"Do you want to buy a new race for {horse} for {horse.new_race_price} Kč? [Y/n] ")
        return key == "y" or key is "Y" or key == ""

