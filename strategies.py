from abc import ABC, abstractmethod
from board import Horse, Trainer


class Strategy(ABC):
    @abstractmethod
    def decide_whether_to_buy_property(self, controller, property):
        pass

    @abstractmethod
    def decide_whether_to_buy_race(self, controller, horse):
        pass


class ThresholdStrategy(Strategy):
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


class ScoreStrategy(Strategy):
    """
    This strategy assigns a score to every property that is offered to it.
    The score is computed by a set of rules, depending on how the property
    meets them. If the score is positive, the property is bought.
    """
    def decide_whether_to_buy_property(self, controller, property):
        score = 0
        player_name = controller.player_name

        remaining_money = controller.player_money - property.price
        money_scores = {
            100000: 10,
            50000: 7,
            30000: 6,
            25000: 5,
            20000: 4,
            10000: 3,
            5000: 2,
            3000: 0,
            2000: -1,
            1000: -3,
            0: -5
        }
        score += self.__determine_score(money_scores, remaining_money)

        if isinstance(property, Horse):
            horse_efficiency = property.admissions[0] / property.price
            horse_efficiency_scores = {
                1.25: 3,
                1: 2.5,
                .8: 1,
                .7: .5,
                .5: 0,
                .3: -2,
                0: -3
            }
            score += self.__determine_score(horse_efficiency_scores, horse_efficiency)

            main_race_efficiency = property.admissions[5] / 5 * property.new_race_price
            race_efficiency_scores = {
                2.4: 5,
                2.2: 4,
                2: 3,
                1.8: 2,
                1.6: 1,
                1.4: 0,
                1: -2,
                0: -3
            }
            score += self.__determine_score(
                race_efficiency_scores,
                main_race_efficiency
            )

            stable = property.stable
            stable_owned =\
                controller.number_of_horses_of_stable_owned_by_player(player_name, stable)\
                / controller.number_of_horses_of_stable(stable)
            stable_owned_scores = {
                1: 5,
                2/3: 4,
                1/2: 3,
                1/3: 1,
                0: -1
            }
            score += self.__determine_score(
                stable_owned_scores,
                stable_owned
            )

        elif isinstance(property, Trainer):
            score += 2

            trainers_owned =\
                controller.number_of_trainers_already_owned_by_player(player_name)
            trainers_owned_scores = {
                3: 5,
                2: 3,
                1: 0,
                0: -1
            }
            score += self.__determine_score(
                trainers_owned_scores,
                trainers_owned
            )

        return score > 0

    def decide_whether_to_buy_race(self, controller, horse):
        score = 0
        remaining_money = controller.player_money - horse.price

        money_scores = {
            100000: 10,
            50000: 7,
            30000: 6,
            25000: 5,
            20000: 4,
            10000: 3,
            5000: 2,
            3000: 0,
            2000: -1,
            1000: -3,
            0: -5
        }
        score += self.__determine_score(money_scores, remaining_money)

        main_race_efficiency = horse.admissions[5] / 5 * horse.new_race_price
        race_efficiency_scores = {
            2.4: 5,
            2.2: 4,
            2: 3,
            1.8: 2,
            1.6: 1,
            1.4: 0,
            1: -2,
            0: -3
        }
        score += self.__determine_score(
            race_efficiency_scores,
            main_race_efficiency
        )

        return score > 0

    @staticmethod
    def __determine_score(thresholds, actual):
        for threshold, delta_score in thresholds.items():
            if threshold <= actual:
                return delta_score


class HumanStrategy(Strategy):
    """Buys what you tell him to buy."""

    def decide_whether_to_buy_property(self, controller, property):
        key = input(f"Do you want to buy {property} for {property.price} Kč? [Y/n] ")
        return key == "y" or key == "Y" or key == ""

    def decide_whether_to_buy_race(self, controller, horse):
        key = input(f"Do you want to buy a new race for {horse} for {horse.new_race_price} Kč? [Y/n] ")
        return key == "y" or key == "Y" or key == ""
