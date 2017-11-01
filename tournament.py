#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import ThresholdStrategy, NoCheapHorsesStrategy, ScoreStrategy
import itertools
import logger
import math

logger.enabled = False

strategies = [
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
]

number_of_players = 3
set_length = 10

combinations = itertools.combinations(strategies, number_of_players)

number_of_games = math.factorial(len(strategies))\
                  // math.factorial(number_of_players)\
                  // math.factorial(len(strategies) - number_of_players)\
                  * set_length

number_of_games_of_one_player = math.factorial(len(strategies) - 1) \
                  // math.factorial(number_of_players - 1) \
                  // math.factorial(len(strategies) - number_of_players) \
                  * set_length

number_of_games_by_players = {}
wins = {}

for strategy in strategies:
    number_of_games_by_players[strategy[1]] = 0
    wins[strategy[1]] = 0

ties = 0

for combination in combinations:
    for i in range(set_length):
        players = [Player(player[1], player[0]) for player in combination]
        game = Game(players)
        rank = game.play()
        if rank:
            wins[rank[0]] += 1
            for player in rank:
                number_of_games_by_players[player] += 1
        else:
            ties += 1

print(f"The rank for {number_of_games} games ({number_of_games // set_length} combinations, {ties} ties):")

output_file = open("./stats.txt", "w")

for player in sorted(wins, key=wins.get, reverse=True):
    score = wins[player]
    game_played = number_of_games_by_players[player]
    print(f"{player}: {score} ({100 * score // game_played}%, {game_played} games)")
    output_file.write(f"{player} {score} {game_played}\n")

output_file.close()
