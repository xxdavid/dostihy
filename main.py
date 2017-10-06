#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import BuyAllStrategy, BuyNothingStrategy, CautiousStrategy
import logger

logger.enabled = True

game = Game([
    Player("Donald", BuyAllStrategy(), "red"),
    Player("Hillary", CautiousStrategy(15000), "yellow"),
    Player("Bernie", BuyNothingStrategy(), "blue"),
])

rank = game.play()
