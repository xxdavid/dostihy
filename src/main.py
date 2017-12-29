#!/usr/bin/env python3
from game import Game
from player import Player
from strategies import ThresholdStrategy
import logger

logger.enabled = True

game = Game([
    Player("Donald", ThresholdStrategy(0), "red"),
    Player("Hillary", ThresholdStrategy(3000), "yellow"),
    Player("Bernie", ThresholdStrategy(60000), "blue"),
])

rank = game.play()
