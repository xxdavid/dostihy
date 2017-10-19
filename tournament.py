#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import BuyAllStrategy, BuyNothingStrategy, CautiousStrategy, NoCheapHorsesStrategy
import itertools
import logger

logger.enabled = False

strategies = [
    [BuyNothingStrategy(), "BuyNothing"],
    [BuyAllStrategy(), "BuyAll"],
    [CautiousStrategy(500), "Cautious500"],
    [CautiousStrategy(1000), "Cautious1000"],
    [CautiousStrategy(2000), "Cautious2000"],
    [CautiousStrategy(3000), "Cautious3000"],
    [CautiousStrategy(4000), "Cautious4000"],
    [CautiousStrategy(5000), "Cautious5000"],
    [CautiousStrategy(10000), "Cautious10000"],
    [CautiousStrategy(15000), "Cautious15000"],
    [CautiousStrategy(20000), "Cautious20000"],
    [NoCheapHorsesStrategy(), "NoCheapHorses"],
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
