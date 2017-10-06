from board import initialBoard
from random import randint, shuffle
from logger import log, log_event
from copy import deepcopy


def throw_die():
    return randint(1, 6)


class Game:
    def __init__(self, players):
        self.players = players
        self.board = deepcopy(initialBoard)
        self.round = 0
        self.rank = []
        self.bank = 200000 - (len(players) * 30000)

        shuffle(self.players)

    def play(self):
        for self.round in range(1, 1000):
            for player in self.players:
                self.play_turn(player)
                if player.money < 0:
                    log_event(player, "BANKRUPTED")
                    self.players.remove(player)
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

        return False  # the game failed and no one won

    def play_turn(self, player):
        die = throw_die()
        if die == 6:
            die += throw_die()
            # TODO: if die == 12: "Distanc"
        self.move_player(player, die)

    def move_player(self, player, number_of_steps):
        player.position += number_of_steps
        if player.position > (len(self.board) - 1):
            player.position -= len(self.board)
            if self.bank > 4000:
                self.bank -= 4000
                player.money += 4000  # bonus for crossing the start field
                log_event(player, "received a bonus of 4000 Kč for crossing the start field")
        field = self.board[player.position]
        log_event(player, f"threw {number_of_steps} and moved to {field.name}")
        field.visit(player, self.board)

    def report_state(self):
        state_report = f"State after round {self.round} -- "
        state_report += ", ".join(map(lambda p: f"{p}: {'{:,}'.format(p.money)} Kč", self.players))
        log(state_report + "\n", "white")
