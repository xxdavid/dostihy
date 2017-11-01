#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import ThresholdStrategy, NoCheapHorsesStrategy, ScoreStrategy
import itertools
import logger
import math


class Tournament:
    def __init__(self, number_of_players, set_length, strategies):
        self.number_of_players = number_of_players
        self.set_length = set_length
        self.strategies = strategies

        self.combinations = self.compute_combinations()
        self.number_of_combinations = self.compute_number_of_combinations()
        self.total_number_of_games = self.number_of_combinations * self.set_length
        self.number_of_games_of_one_player = self.compute_number_of_games_of_one_player()
        self.number_of_ties = 0

        self.number_of_games_by_players = {}
        self.wins = {}
        for strategy in self.strategies:
            self.number_of_games_by_players[strategy[1]] = 0
            self.wins[strategy[1]] = 0

        logger.enabled = False

    def start(self):
        self.print_info()
        self.play()
        self.print_results()
        self.write_results_to_file()

    def play(self):
        for combination in self.combinations:
            for i in range(self.set_length):
                players = [Player(player[1], player[0]) for player in combination]
                game = Game(players)
                rank = game.play()
                if rank:
                    self.wins[rank[0]] += 1
                    for player in rank:
                        self.number_of_games_by_players[player] += 1
                else:
                    self.number_of_ties += 1

    def compute_combinations(self):
        return itertools.combinations(self.strategies, self.number_of_players)

    def compute_number_of_combinations(self):
        return math.factorial(len(self.strategies)) \
               // math.factorial(self.number_of_players) \
               // math.factorial(len(self.strategies) - self.number_of_players)

    def compute_number_of_games_of_one_player(self):
        return math.factorial(len(self.strategies) - 1) \
                // math.factorial(self.number_of_players - 1) \
                // math.factorial(len(self.strategies) - self.number_of_players) \
                * self.set_length

    def print_info(self):
        print(f"The tournament will consist of {self.total_number_of_games} "
              f"({self.number_of_combinations} combinations * {self.set_length} rounds).")
        print(f"Each player will play {self.number_of_games_of_one_player} games.")
        print("Starting to play.")

    def print_results(self):
        print("The tournament has ended.")
        ties_percentage = 100 * self.number_of_ties // self.total_number_of_games
        print(f"There were {self.number_of_ties} ties in total,"
              f"that's {ties_percentage}% of the all games.")

        print("\nThe ranks are:")
        for player in sorted(self.wins, key=self.wins.get, reverse=True):
            score = self.wins[player]
            game_played = self.number_of_games_by_players[player]
            print(f"{player}: {score} ({100 * score // game_played}%, {game_played} non-tie games)")

    def write_results_to_file(self):
        file = open("./stats.txt", "w")

        file.write(str(self.number_of_combinations) + "\n")
        file.write(str(self.set_length) + "\n")
        file.write(str(self.number_of_games_of_one_player) + "\n\n")

        for player in sorted(self.wins, key=self.wins.get, reverse=True):
            score = self.wins[player]
            game_played = self.number_of_games_by_players[player]
            file.write(f"{player} {score} {game_played}\n")

        file.close()


Tournament(3, 10, [
    [ThresholdStrategy(0), "Threshold0"],
    [ThresholdStrategy(500), "Threshold500"],
    [ThresholdStrategy(1000), "Threshold1000"],
    [ThresholdStrategy(2000), "Threshold2000"],
    [ThresholdStrategy(3000), "Threshold3000"],
    [ThresholdStrategy(4000), "Threshold4000"],
    [ThresholdStrategy(5000), "Threshold5000"],
    [ThresholdStrategy(10000), "Threshold10000"],
    [ThresholdStrategy(15000), "Threshold15000"],
    [ThresholdStrategy(20000), "Threshold20000"],
    [ThresholdStrategy(60000), "Threshold60000"],
    [NoCheapHorsesStrategy(), "NoCheapHorses"],
    [ScoreStrategy(), "ScoreStrategy"],
]).start()
