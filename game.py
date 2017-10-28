from board import initialBoard
from random import randint, shuffle
from logger import log, log_event
from copy import deepcopy
from board import Horse, Trainer, Property, SuspensionField


def throw_die():
    return randint(1, 6)


class Game:
    def __init__(self, players):
        self.players = players
        self.board = deepcopy(initialBoard)
        self.round = 0
        self.rank = []
        self.bank_money = 200000 - (len(players) * 30000)
        self.current_player = None
        self.controller = self.Controller(self)

        shuffle(self.players)

    def play(self):
        for self.round in range(1, 500):
            for player in self.players:
                self.current_player = player
                self.play_turn(player)
                if player.money < 0:
                    log_event(player, "BANKRUPTED")
                    self.players.remove(player)
                    self.bank_money += player.money
                    self.free_losers_properties(player)
                    self.rank.insert(0, player.name)

                    if len(self.players) == 1:
                        self.report_state()
                        winner = self.players[0]
                        self.rank.insert(0, winner.name)
                        log(f"{winner.name.upper()} WON, congrats!", "green")
                        log("\nRank:", "cyan")
                        for index, player_name in enumerate(self.rank):
                            log(f"{index + 1}. {player_name}", "cyan")
                        return self.rank

            self.report_state()

        return False  # the game failed and no one won -> tie

    def play_turn(self, player):
        if not player.suspended:
            die = throw_die()
            if die == 6:
                die += throw_die()
            if die == 12:
                log_event(player, f"threw {die} and that means he will be suspended")
                return self.controller.move_player_to_suspension_field(False)
            log_event(player, f"threw {die}")
            self.move_player(player, die)
        else:
            log_event(player, "is suspended")
            die = throw_die()
            if die == 6:
                log(f"{player} threw {die} and is now free again!", player.color)
                player.suspended = False
                self.play_turn(player)
            else:
                log_event(player, f"threw {die} and is still suspended")

    def move_player(self, player, number_of_steps, receives_bonus=True):
        player.position += number_of_steps
        if player.position > (len(self.board) - 1):
            player.position -= len(self.board)
            if self.bank_money > 4000 and receives_bonus:
                self.bank_money -= 4000
                player.money += 4000  # bonus for crossing the start field
                log_event(player, "received a bonus of 4000 Kč for crossing the start field")
        field = self.board[player.position]
        log_event(player, f"moved to {field.name}")
        field.visit(self.controller)

    def report_state(self):
        state_report = f"State after round {self.round} -- "
        state_report += ", ".join(map(lambda p: f"{p}: {'{:,}'.format(p.money)} Kč", self.players))
        log(state_report + "\n", "white")

    def free_losers_properties(self, loser):
        for field in self.board:
            if isinstance(field, Property) and field.owner_name == loser.name:
                field.owner_name = None
                if isinstance(field, Horse):
                    field.races = 0

    class Controller:
        def __init__(self, game):
            self.__game = game

        @property
        def player_name(self):
            return self.__game.current_player.name

        @property
        def player_money(self):
            return self.__game.current_player.money

        @property
        def current_field_index(self):
            return self.__game.current_player.position

        @property
        def current_round(self):
            return self.__game.round

        def __find_player_with_name(self, name):
            for player in self.__game.players:
                if player.name == name:
                    return player

        def ask_player_whether_he_wants_property(self, property):
            # sorry, women and gender neutral players
            player = self.__game.current_player
            return player.strategy.decide_whether_to_buy_property(self, property)

        def ask_player_whether_he_wants_new_race(self, horse):
            player = self.__game.current_player
            return player.strategy.decide_whether_to_buy_race(self, horse)

        def transfer_player_money_to_bank(self, player, amount):
            player.money -= amount
            self.__game.bank_money += amount

        def is_property_owned_by_player(self, property):
            return property.owner_name == self.__game.current_player.name

        def number_of_horses_of_stable_owned_by_player(self, stable, player_name):
            return len([
                field for field in self.__game.board
                if isinstance(field, Horse) and field.stable == stable\
                    and field.owner_name == player_name
            ])

        def number_of_horses_of_stable(self, stable):
            return len([
                field for field in self.__game.board
                if isinstance(field, Horse) and field.stable == stable
            ])

        def is_whole_stable_owned_by_player(self, stable, player_name):
            return self.number_of_horses_of_stable_owned_by_player(stable, player_name)\
                == self.number_of_horses_of_stable(stable)

        def number_of_trainers_already_owned_by_player(self, player_name):
            return len([
                field.owner_name == player_name
                for field in self.__game.board
                if isinstance(field, Trainer) and field.owner_name == player_name
            ])

        def has_player_enough_money(self, amount):
            return self.player_money >= amount

        def is_property_owned_by_another_player(self, property):
            return property.owner_name is not None\
                and not self.is_property_owned_by_player(property)

        def count_number_of_trainers_owned_by_player(self, player_name):
            return sum(
                isinstance(field, Trainer) and field.owner_name == player_name
                for field in self.__game.board
            )

        def is_player_suspended(self, player_name):
            player = self.__find_player_with_name(player_name)
            return player.suspended

        def move_player_to_field(self, field_index, receives_bonus=True):
            player = self.__game.current_player
            if player.position <= field_index:
                steps = field_index - player.position
            else:
                steps = len(self.__game.board) - (player.position - field_index)
            self.__game.move_player(player, steps, receives_bonus)

        def move_player_to_suspension_field(self, receives_bonus=True):
            suspension_index = [
                i
                for i, field
                in enumerate(self.__game.board)
                if isinstance(field, SuspensionField)
            ][0]
            self.move_player_to_field(suspension_index, receives_bonus)

        def buy_property_for_player(self, property):
            player = self.__game.current_player
            price = property.price
            self.transfer_player_money_to_bank(player, price)
            property.owner_name = player.name
            log_event(player, f"bought {property}")

        def buy_new_race_for_player(self, horse):
            player = self.__game.current_player
            price = horse.new_race_price
            self.transfer_player_money_to_bank(player, price)
            horse.races += 1
            log_event(player, f"bought a new race for {horse}")

        def pay_admission_to_another_player(self, receiver_name, amount, purpose):
            player = self.__game.current_player
            receiver = self.__find_player_with_name(receiver_name)
            player.money -= amount
            receiver.money += amount
            log_event(player, f"paid {receiver_name} an admission of {amount} Kč for {purpose}")

        def pay_fee_to_bank(self, amount, purpose):
            player = self.__game.current_player
            self.transfer_player_money_to_bank(player, amount)
            log_event(player, f"paid {amount} Kč for {purpose}")

        def suspend_player(self):
            player = self.__game.current_player
            player.suspended = True
            log_event(player, "suspended")
