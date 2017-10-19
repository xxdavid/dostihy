from abc import ABC, abstractmethod
from board import Horse


class Strategy(ABC):
    @abstractmethod
    def decide_whether_to_buy_property(self, controller, property):
        pass

    @abstractmethod
    def decide_whether_to_buy_race(self, controller, horse):
        pass


class BuyAllStrategy(Strategy):
    """Buys everything it has money for."""
    def decide_whether_to_buy_property(self, controller, property):
        return True

    def decide_whether_to_buy_race(self, controller, horse):
        return True


class BuyNothingStrategy(Strategy):
    """Buys literally nothing. """
    def decide_whether_to_buy_property(self, controller, property):
        return False

    def decide_whether_to_buy_race(self, controller, horse):
        return False


class CautiousStrategy(Strategy):
    """
    Buys offered stuff only if player's amount of money
    won't be below the threshold after the purchase.
    """
    def __init__(self, threshold):
        self.threshold = threshold

    def decide_whether_to_buy_property(self, controller, property):
        return (controller.player_money - property.price) > self.threshold

    def decide_whether_to_buy_race(self, controller, horse):
        return (controller.player_money - horse.new_race_price) > self.threshold




class NoCheapHorsesStrategy(Strategy):
    """
    Buys anything it can afford (= Cautious(2000))
    except the first two horses (the two can be bought only after round 10).
    """
    def decide_whether_to_buy_property(self, controller, property):
        return not (
            isinstance(property, Horse)
            and controller.current_field_index < 3
            and controller.current_round <= 10
        ) and controller.player_money > 2000

    def decide_whether_to_buy_race(self, controller, horse):
        return True

class HumanStrategy(Strategy):
    """Buys what you tell him to buy."""
    def decide_whether_to_buy_property(self, controller, property):
        key = input(f"Do you want to buy {property} for {property.price} Kč? [Y/n] ")
        return key == "y" or key == "Y" or key == ""

    def decide_whether_to_buy_race(self, controller, horse):
        key = input(f"Do you want to buy a new race for {horse} for {horse.new_race_price} Kč? [Y/n] ")
        return key == "y" or key == "Y" or key == ""

