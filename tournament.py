#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import ThresholdStrategy, NoCheapHorsesStrategy, ScoreStrategy
import itertools
import logger

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

wins = {}
for strategy in strategies:
    wins[strategy[1]] = 0

number_of_games = 0
for combination in combinations:
    for i in range(set_length):
        players = [Player(player[1], player[0]) for player in combination]
        game = Game(players)
        rank = game.play()
        if rank:
            wins[rank[0]] += 1
        number_of_games += 1

print(f"The rank for {number_of_games} games ({number_of_games // set_length } combinations):")

output_file = open("./stats.txt", "w")

for w in sorted(wins, key=wins.get, reverse=True):
    print(f"{w}: {wins[w]}")
    output_file.write(f"{w} {wins[w]}\n")

output_file.close()
